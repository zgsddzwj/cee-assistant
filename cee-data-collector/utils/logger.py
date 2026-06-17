# utils/logger.py
"""日志管理器 - 统一日志配置和管理

特性：
1. 结构化日志（JSON格式）
2. 多级别日志
3. 文件轮转
4. 日志分类
"""

import logging
import logging.handlers
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import os

class JSONFormatter(logging.Formatter):
    """JSON格式日志格式化器"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # 添加额外字段
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        # 添加异常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)

class LoggerManager:
    """日志管理器"""
    
    def __init__(self, log_dir: str = './logs', app_name: str = 'cee-assistant'):
        self.log_dir = log_dir
        self.app_name = app_name
        
        os.makedirs(log_dir, exist_ok=True)
        
        # 创建日志目录结构
        self.log_files = {
            'app': os.path.join(log_dir, f'{app_name}.log'),
            'error': os.path.join(log_dir, f'{app_name}.error.log'),
            'access': os.path.join(log_dir, f'{app_name}.access.log'),
        }
    
    def create_logger(self, name: str, level: int = logging.INFO, use_json: bool = False) -> logging.Logger:
        """创建配置好的日志记录器"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
        
        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        if use_json:
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
        
        logger.addHandler(console_handler)
        
        # 文件输出（按大小轮转）
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_files['app'],
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        if use_json:
            file_handler.setFormatter(JSONFormatter())
        else:
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
        
        logger.addHandler(file_handler)
        
        # 错误日志（单独文件）
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_files['error'],
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(exc_info)s'
        ))
        
        logger.addHandler(error_handler)
        
        return logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """获取日志记录器"""
        return logging.getLogger(name)

# 全局日志管理器实例
logger_manager = LoggerManager()

def get_logger(name: str) -> logging.Logger:
    """获取日志记录器的便捷函数"""
    return logger_manager.get_logger(name)
