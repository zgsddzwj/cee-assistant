# core/scheduler.py
from typing import Dict, List, Optional
import threading
import time
import json
from datetime import datetime

class DataScheduler:
    """数据调度中心 - 统一管理所有采集任务的执行周期
    
    支持：
    1. 定时任务调度（考试院、院校、第三方API）
    2. 手动触发采集
    3. 任务状态监控
    """
    
    def __init__(self, data_dir: str = './data'):
        self.data_dir = data_dir
        self.jobs: Dict[str, dict] = {}
        self._running = False
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
                'status': 'idle',
            },
            'university_spider': {
                'name': 'university_spider',
                'description': '院校招生计划和专业信息采集',
                'interval': 168 * 60 * 60,  # 7 days
                'last_run': None,
                'enabled': True,
                'status': 'idle',
            },
            'third_party_api': {
                'name': 'third_party_api',
                'description': '第三方数据平台API采集',
                'interval': 6 * 60 * 60,  # 6 hours
                'last_run': None,
                'enabled': False,  # 默认关闭，需要API key
                'status': 'idle',
            }
        }
    
    def start(self):
        """启动调度器（后台线程模式）"""
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler)
        self._scheduler_thread.daemon = True
        self._scheduler_thread.start()
        print("[Scheduler] Started")
    
    def stop(self):
        """停止调度器"""
        self._running = False
        if hasattr(self, '_scheduler_thread'):
            self._scheduler_thread.join(timeout=5)
        print("[Scheduler] Stopped")
    
    def _run_scheduler(self):
        """调度器主循环"""
        while self._running:
            current_time = time.time()
            for job_name, job_config in self.jobs.items():
                if not job_config['enabled']:
                    continue
                    
                if (job_config['last_run'] is None or 
                    current_time - job_config['last_run'] >= job_config['interval']):
                    self._execute_job(job_name)
                    job_config['last_run'] = current_time
            
            time.sleep(60)  # 每分钟检查一次
    
    def _execute_job(self, job_name: str):
        """执行指定任务"""
        job = self.jobs.get(job_name)
        if not job:
            return
        
        job['status'] = 'running'
        print(f"[Scheduler] Executing job: {job_name} - {job['description']}")
        
        try:
            if job_name == 'exam_board_spider':
                self._run_exam_board_spider()
            elif job_name == 'university_spider':
                self._run_university_spider()
            elif job_name == 'third_party_api':
                self._run_third_party_api()
            
            job['status'] = 'completed'
            print(f"[Scheduler] Job {job_name} completed")
        except Exception as e:
            job['status'] = 'failed'
            print(f"[Scheduler] Job {job_name} failed: {e}")
    
    def _run_exam_board_spider(self):
        """运行考试院爬虫"""
        from spiders.exam_board_spider import ExamBoardSpider
        spider = ExamBoardSpider(use_mock=True, data_dir=self.data_dir)
        spider.run(year=2024, save=True)
    
    def _run_university_spider(self):
        """运行院校爬虫"""
        from spiders.university_spider import UniversitySpider
        spider = UniversitySpider(use_mock=True, data_dir=self.data_dir)
        spider.run(year=2024, save=True)
    
    def _run_third_party_api(self):
        """运行第三方API采集"""
        print("[Scheduler] Third party API job not implemented yet")
    
    def run_job_now(self, job_name: str) -> bool:
        """手动立即执行某个任务"""
        if job_name not in self.jobs:
            print(f"[Scheduler] Unknown job: {job_name}")
            return False
        
        self._execute_job(job_name)
        return True
    
    def get_job_status(self) -> Dict:
        """获取所有任务状态"""
        status = {}
        for name, job in self.jobs.items():
            status[name] = {
                'name': job['name'],
                'description': job['description'],
                'enabled': job['enabled'],
                'status': job['status'],
                'last_run': datetime.fromtimestamp(job['last_run']).isoformat() if job['last_run'] else None,
                'interval_hours': job['interval'] / 3600,
            }
        return status
    
    def enable_job(self, job_name: str):
        """启用任务"""
        if job_name in self.jobs:
            self.jobs[job_name]['enabled'] = True
            print(f"[Scheduler] Job {job_name} enabled")
    
    def disable_job(self, job_name: str):
        """禁用任务"""
        if job_name in self.jobs:
            self.jobs[job_name]['enabled'] = False
            print(f"[Scheduler] Job {job_name} disabled")


def main():
    """命令行入口"""
    import sys
    
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
        elif command == 'start':
            scheduler.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python -m core.scheduler [run|status|start]")
    else:
        # 默认运行所有任务一次
        print("Running all enabled jobs...")
        for job_name in scheduler.jobs:
            if scheduler.jobs[job_name]['enabled']:
                scheduler.run_job_now(job_name)


if __name__ == '__main__':
    main()
