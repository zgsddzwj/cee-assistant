#!/usr/bin/env python3
"""CEE Data Collector CLI 工具

提供命令行接口用于数据采集、管理和监控。

用法:
    python -m cli --help
    python -m cli generate-data --year 2024
    python -m cli run-spider --type exam-board
    python -m cli status
    python -m cli monitor
"""

import argparse
import sys
import json
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cmd_generate_data(args):
    """生成模拟数据命令"""
    from data_generator import generate_all_data
    
    print(f"Generating mock data for year {args.year}...")
    summary = generate_all_data(year=args.year, data_dir=args.dir)
    
    print("\n=== Data Generation Summary ===")
    print(json.dumps(summary['statistics'], ensure_ascii=False, indent=2))
    print(f"\nData saved to: {args.dir}")

def cmd_run_spider(args):
    """运行爬虫命令"""
    from core.scheduler import DataScheduler
    
    scheduler = DataScheduler(data_dir=args.dir)
    
    if args.type == 'exam-board':
        job_name = 'exam_board_spider'
    elif args.type == 'university':
        job_name = 'university_spider'
    elif args.type == 'all':
        job_name = None
    else:
        print(f"Unknown spider type: {args.type}")
        sys.exit(1)
    
    if job_name:
        print(f"Running spider: {job_name}")
        scheduler.run_job_now(job_name)
    else:
        print("Running all spiders...")
        for job_name in scheduler.jobs:
            if scheduler.jobs[job_name]['enabled']:
                scheduler.run_job_now(job_name)

def cmd_status(args):
    """查看状态命令"""
    from core.scheduler import DataScheduler
    from core.storage import StorageManager
    import os
    
    scheduler = DataScheduler(data_dir=args.dir)
    storage = StorageManager(data_dir=args.dir)
    
    print("=== Scheduler Status ===")
    print(json.dumps(scheduler.get_job_status(), ensure_ascii=False, indent=2))
    
    print("\n=== Storage Status ===")
    print(json.dumps(storage.get_storage_status(), ensure_ascii=False, indent=2))
    
    print("\n=== Data Files ===")
    if os.path.exists(args.dir):
        files = sorted(os.listdir(args.dir))
        for f in files:
            filepath = os.path.join(args.dir, f)
            size = os.path.getsize(filepath)
            print(f"  {f} ({size:,} bytes)")
    else:
        print("  No data directory found")

def cmd_monitor(args):
    """监控命令"""
    from utils.monitor import monitor
    
    print("=== System Health ===")
    health = monitor.get_system_health()
    print(json.dumps(health, ensure_ascii=False, indent=2))
    
    print("\n=== Metrics Summary ===")
    summary = monitor.get_metrics_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    if args.export:
        monitor.export_metrics(args.export)
        print(f"\nMetrics exported to {args.export}")

def cmd_validate(args):
    """验证数据命令"""
    from core.pipeline import DataPipeline, DataType
    import json
    
    pipeline = DataPipeline()
    
    print(f"Validating data file: {args.file}")
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
    
    if not isinstance(data, list):
        print("Data must be a list")
        sys.exit(1)
    
    # 确定数据类型
    data_type = DataType(args.type) if args.type else None
    if not data_type:
        # 自动推断
        if 'batch' in data[0]:
            data_type = DataType.SCORE
        elif 'cumulative_count' in data[0]:
            data_type = DataType.RANK
        elif 'university_name' in data[0]:
            data_type = DataType.UNIVERSITY
        elif 'admission_score' in data[0]:
            data_type = DataType.MAJOR
        else:
            print("Cannot determine data type, please specify with --type")
            sys.exit(1)
    
    result = pipeline.validate_batch(data, data_type)
    
    print(f"\n=== Validation Result ===")
    print(f"Total items: {len(data)}")
    print(f"Valid: {result['valid_count']}")
    print(f"Invalid: {result['invalid_count']}")
    print(f"Success rate: {result['success_rate']:.1%}")
    
    if result['invalid_count'] > 0 and args.verbose:
        print("\n=== Invalid Items ===")
        for item in result['invalid'][:10]:  # 只显示前10个
            print(f"  Data: {item['data']}")
            print(f"  Errors: {item['errors']}")
            print()

def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description='CEE Data Collector CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate-data --year 2024
  %(prog)s run-spider --type exam-board
  %(prog)s status
  %(prog)s monitor --export metrics.json
  %(prog)s validate data/all_scores_2024.json --type score
        """
    )
    
    parser.add_argument('--dir', default='./data', help='Data directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # generate-data 命令
    gen_parser = subparsers.add_parser('generate-data', help='Generate mock data')
    gen_parser.add_argument('--year', type=int, default=2024, help='Year to generate')
    gen_parser.set_defaults(func=cmd_generate_data)
    
    # run-spider 命令
    spider_parser = subparsers.add_parser('run-spider', help='Run spider')
    spider_parser.add_argument('--type', choices=['exam-board', 'university', 'all'], 
                                default='all', help='Spider type')
    spider_parser.set_defaults(func=cmd_run_spider)
    
    # status 命令
    status_parser = subparsers.add_parser('status', help='Show system status')
    status_parser.set_defaults(func=cmd_status)
    
    # monitor 命令
    monitor_parser = subparsers.add_parser('monitor', help='System monitoring')
    monitor_parser.add_argument('--export', help='Export metrics to file')
    monitor_parser.set_defaults(func=cmd_monitor)
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='Validate data file')
    validate_parser.add_argument('file', help='Data file to validate')
    validate_parser.add_argument('--type', choices=['score', 'rank', 'university', 'major'],
                                help='Data type (auto-detect if not specified)')
    validate_parser.set_defaults(func=cmd_validate)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        logger.error(f"Command failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
