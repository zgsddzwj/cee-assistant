# core/scheduler.py
from typing import Dict, List, Optional, Callable
import threading
import time
import json
import logging
from datetime import datetime
from enum import Enum

class JobStatus(Enum):
    """任务状态枚举"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DISABLED = "disabled"

class DataScheduler:
    """数据调度中心 - 统一管理所有采集任务的执行周期
    
    特性：
    1. 定时任务调度（支持间隔执行）
    2. 手动触发执行
    3. 任务状态监控和日志记录
    4. 异常处理和重试机制
    5. 任务执行历史记录
    """
    
    def __init__(self, data_dir: str = './data', log_level: int = logging.INFO):
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        self.jobs: Dict[str, dict] = {}
        self._running = False
        self._scheduler_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._execution_history: List[Dict] = []
        
        self._initialize_jobs()
        
    def _initialize_jobs(self):
        """初始化默认采集任务"""
        self.jobs = {
            'exam_board_spider': {
                'name': 'exam_board_spider',
                'description': '各省市考试院分数线和一分一段表采集',
                'interval': 24 * 60 * 60,  # 24 hours
                'last_run': None,
                'enabled': True,
                'status': JobStatus.IDLE,
                'retry_count': 0,
                'max_retries': 3,
            },
            'university_spider': {
                'name': 'university_spider',
                'description': '院校招生计划和专业信息采集',
                'interval': 168 * 60 * 60,  # 7 days
                'last_run': None,
                'enabled': True,
                'status': JobStatus.IDLE,
                'retry_count': 0,
                'max_retries': 3,
            },
            'third_party_api': {
                'name': 'third_party_api',
                'description': '第三方数据平台API采集',
                'interval': 6 * 60 * 60,  # 6 hours
                'last_run': None,
                'enabled': False,  # 默认关闭，需要API key
                'status': JobStatus.DISABLED,
                'retry_count': 0,
                'max_retries': 3,
            }
        }
    
    def start(self):
        """启动调度器（后台线程模式）"""
        if self._running:
            self.logger.warning("Scheduler is already running")
            return
            
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
        self.logger.info("[Scheduler] Started")
    
    def stop(self):
        """停止调度器"""
        if not self._running:
            return
            
        self._running = False
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduler_thread.join(timeout=5)
        self.logger.info("[Scheduler] Stopped")
    
    def _run_scheduler(self):
        """调度器主循环"""
        self.logger.info("[Scheduler] Main loop started")
        
        while self._running:
            try:
                current_time = time.time()
                
                with self._lock:
                    for job_name, job_config in self.jobs.items():
                        if not job_config['enabled']:
                            continue
                            
                        if (job_config['last_run'] is None or 
                            current_time - job_config['last_run'] >= job_config['interval']):
                            self._execute_job(job_name)
                            job_config['last_run'] = current_time
                
                # 每分钟检查一次
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"[Scheduler] Error in main loop: {e}")
                time.sleep(60)  # 出错后等待1分钟再试
    
    def _execute_job(self, job_name: str):
        """执行指定任务"""
        job = self.jobs.get(job_name)
        if not job:
            self.logger.error(f"[Scheduler] Unknown job: {job_name}")
            return
        
        job['status'] = JobStatus.RUNNING
        job['retry_count'] = 0
        start_time = time.time()
        
        self.logger.info(f"[Scheduler] Executing job: {job_name} - {job['description']}")
        
        try:
            if job_name == 'exam_board_spider':
                self._run_exam_board_spider()
            elif job_name == 'university_spider':
                self._run_university_spider()
            elif job_name == 'third_party_api':
                self._run_third_party_api()
            
            job['status'] = JobStatus.COMPLETED
            job['retry_count'] = 0
            
            execution_time = time.time() - start_time
            self.logger.info(f"[Scheduler] Job {job_name} completed in {execution_time:.2f}s")
            
            # 记录执行历史
            self._record_execution(job_name, True, execution_time)
            
        except Exception as e:
            job['retry_count'] += 1
            execution_time = time.time() - start_time
            
            if job['retry_count'] >= job['max_retries']:
                job['status'] = JobStatus.FAILED
                self.logger.error(f"[Scheduler] Job {job_name} failed after {job['max_retries']} retries: {e}")
            else:
                job['status'] = JobStatus.IDLE
                self.logger.warning(f"[Scheduler] Job {job_name} failed (attempt {job['retry_count']}/{job['max_retries']}): {e}")
            
            self._record_execution(job_name, False, execution_time, str(e))
    
    def _record_execution(self, job_name: str, success: bool, duration: float, error: str = None):
        """记录任务执行历史"""
        record = {
            'job_name': job_name,
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'duration': duration,
        }
        if error:
            record['error'] = error
        
        self._execution_history.append(record)
        
        # 只保留最近100条记录
        if len(self._execution_history) > 100:
            self._execution_history = self._execution_history[-100:]
    
    def _run_exam_board_spider(self):
        """运行考试院爬虫"""
        from spiders.exam_board_spider import ExamBoardSpider
        from core.config import config
        
        spider = ExamBoardSpider(
            use_mock=config.mock_mode,
            data_dir=self.data_dir
        )
        spider.run(year=config.default_year, save=True)
    
    def _run_university_spider(self):
        """运行院校爬虫"""
        from spiders.university_spider import UniversitySpider
        from core.config import config
        
        spider = UniversitySpider(
            use_mock=config.mock_mode,
            data_dir=self.data_dir
        )
        spider.run(year=config.default_year, save=True)
    
    def _run_third_party_api(self):
        """运行第三方API采集"""
        self.logger.info("[Scheduler] Third party API job not implemented yet")
    
    def run_job_now(self, job_name: str) -> bool:
        """手动立即执行某个任务"""
        if job_name not in self.jobs:
            self.logger.error(f"[Scheduler] Unknown job: {job_name}")
            return False
        
        self.logger.info(f"[Scheduler] Manually triggering job: {job_name}")
        self._execute_job(job_name)
        return True
    
    def get_job_status(self) -> Dict:
        """获取所有任务状态"""
        status = {}
        with self._lock:
            for name, job in self.jobs.items():
                status[name] = {
                    'name': job['name'],
                    'description': job['description'],
                    'enabled': job['enabled'],
                    'status': job['status'].value,
                    'last_run': datetime.fromtimestamp(job['last_run']).isoformat() if job['last_run'] else None,
                    'interval_hours': job['interval'] / 3600,
                    'retry_count': job['retry_count'],
                    'max_retries': job['max_retries'],
                }
        return status
    
    def get_execution_history(self, job_name: str = None, limit: int = 10) -> List[Dict]:
        """获取任务执行历史"""
        history = self._execution_history
        
        if job_name:
            history = [h for h in history if h['job_name'] == job_name]
        
        return history[-limit:]
    
    def enable_job(self, job_name: str):
        """启用任务"""
        if job_name in self.jobs:
            self.jobs[job_name]['enabled'] = True
            self.jobs[job_name]['status'] = JobStatus.IDLE
            self.logger.info(f"[Scheduler] Job {job_name} enabled")
    
    def disable_job(self, job_name: str):
        """禁用任务"""
        if job_name in self.jobs:
            self.jobs[job_name]['enabled'] = False
            self.jobs[job_name]['status'] = JobStatus.DISABLED
            self.logger.info(f"[Scheduler] Job {job_name} disabled")


def main():
    """命令行入口"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    scheduler = DataScheduler()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'run':
            job_name = sys.argv[2] if len(sys.argv) > 2 else None
            if job_name:
                scheduler.run_job_now(job_name)
            else:
                print("Usage: python -m core.scheduler run <job_name>")
                print("Available jobs:", list(scheduler.jobs.keys()))
        elif command == 'status':
            print(json.dumps(scheduler.get_job_status(), ensure_ascii=False, indent=2))
        elif command == 'history':
            job_name = sys.argv[2] if len(sys.argv) > 2 else None
            history = scheduler.get_execution_history(job_name)
            print(json.dumps(history, ensure_ascii=False, indent=2))
        elif command == 'start':
            scheduler.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python -m core.scheduler [run|status|history|start]")
    else:
        # 默认运行所有启用的任务一次
        print("Running all enabled jobs...")
        for job_name in scheduler.jobs:
            if scheduler.jobs[job_name]['enabled']:
                scheduler.run_job_now(job_name)


if __name__ == '__main__':
    main()
