# utils/monitor.py
"""监控模块 - 系统性能监控和指标收集

特性：
1. 性能指标收集（内存、CPU、时间）
2. 任务执行统计
3. 健康检查
4. 简单的指标导出
"""

import time
import psutil
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from functools import wraps
import logging

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """性能指标"""
    start_time: float
    end_time: Optional[float] = None
    memory_start: Optional[float] = None
    memory_end: Optional[float] = None
    cpu_percent: Optional[float] = None
    
    @property
    def duration(self) -> float:
        """执行时长（秒）"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    @property
    def memory_used(self) -> Optional[float]:
        """内存使用量（MB）"""
        if self.memory_start and self.memory_end:
            return self.memory_end - self.memory_start
        return None

class Monitor:
    """系统监控器"""
    
    def __init__(self):
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
    def start_monitoring(self, task_name: str) -> PerformanceMetrics:
        """开始监控任务"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        metrics = PerformanceMetrics(
            start_time=time.time(),
            memory_start=memory_info.rss / 1024 / 1024,  # MB
        )
        
        logger.debug(f"[Monitor] Started monitoring: {task_name}")
        return metrics
    
    def stop_monitoring(self, metrics: PerformanceMetrics, task_name: str) -> Dict[str, Any]:
        """停止监控并记录指标"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        metrics.end_time = time.time()
        metrics.memory_end = memory_info.rss / 1024 / 1024
        metrics.cpu_percent = process.cpu_percent()
        
        result = {
            'task_name': task_name,
            'timestamp': datetime.now().isoformat(),
            'duration': metrics.duration,
            'memory_start_mb': metrics.memory_start,
            'memory_end_mb': metrics.memory_end,
            'memory_used_mb': metrics.memory_used,
            'cpu_percent': metrics.cpu_percent,
        }
        
        self.metrics_history.append(result)
        
        # 限制历史记录大小
        if len(self.metrics_history) > self.max_history:
            self.metrics_history = self.metrics_history[-self.max_history:]
        
        logger.info(
            f"[Monitor] Task {task_name} completed: "
            f"duration={metrics.duration:.2f}s, "
            f"memory={metrics.memory_used:.2f}MB, "
            f"cpu={metrics.cpu_percent:.1f}%"
        )
        
        return result
    
    def monitor_task(self, func):
        """任务监控装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            task_name = f"{func.__name__}"
            metrics = self.start_monitoring(task_name)
            
            try:
                result = func(*args, **kwargs)
                self.stop_monitoring(metrics, task_name)
                return result
            except Exception as e:
                self.stop_monitoring(metrics, task_name)
                logger.error(f"[Monitor] Task {task_name} failed: {e}")
                raise
        
        return wrapper
    
    def get_system_health(self) -> Dict[str, Any]:
        """获取系统健康状态"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'cores': psutil.cpu_count(),
            },
            'memory': {
                'total_gb': memory.total / 1024 / 1024 / 1024,
                'used_gb': memory.used / 1024 / 1024 / 1024,
                'percent': memory.percent,
            },
            'disk': {
                'total_gb': disk.total / 1024 / 1024 / 1024,
                'used_gb': disk.used / 1024 / 1024 / 1024,
                'percent': disk.percent,
            },
        }
    
    def get_metrics_summary(self, task_name: Optional[str] = None) -> Dict[str, Any]:
        """获取指标汇总"""
        metrics = self.metrics_history
        
        if task_name:
            metrics = [m for m in metrics if m['task_name'] == task_name]
        
        if not metrics:
            return {'count': 0}
        
        durations = [m['duration'] for m in metrics]
        memory_used = [m['memory_used_mb'] for m in metrics if m['memory_used_mb'] is not None]
        
        return {
            'count': len(metrics),
            'duration': {
                'avg': sum(durations) / len(durations),
                'min': min(durations),
                'max': max(durations),
                'total': sum(durations),
            },
            'memory': {
                'avg_mb': sum(memory_used) / len(memory_used) if memory_used else 0,
                'min_mb': min(memory_used) if memory_used else 0,
                'max_mb': max(memory_used) if memory_used else 0,
            },
        }
    
    def export_metrics(self, filename: str = 'metrics.json'):
        """导出指标到文件"""
        import json
        
        data = {
            'system_health': self.get_system_health(),
            'metrics_summary': self.get_metrics_summary(),
            'recent_metrics': self.metrics_history[-100:],  # 最近100条
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"[Monitor] Metrics exported to {filename}")

# 全局监控实例
monitor = Monitor()
