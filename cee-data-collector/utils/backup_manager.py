# utils/backup_manager.py
"""数据备份和恢复管理

支持：
1. 数据备份（压缩）
2. 数据恢复
3. 备份版本管理
4. 自动清理旧备份
"""

import os
import json
import shutil
import zipfile
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class BackupManager:
    """备份管理器"""
    
    def __init__(self, data_dir: str = './data', backup_dir: str = './backups'):
        self.data_dir = data_dir
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, name: Optional[str] = None) -> str:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name or f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # 创建备份目录
        os.makedirs(backup_path, exist_ok=True)
        
        # 复制数据文件
        if os.path.exists(self.data_dir):
            for filename in os.listdir(self.data_dir):
                src = os.path.join(self.data_dir, filename)
                dst = os.path.join(backup_path, filename)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
        
        # 创建备份信息文件
        info = {
            "name": backup_name,
            "created_at": datetime.now().isoformat(),
            "data_dir": self.data_dir,
            "files": os.listdir(backup_path) if os.path.exists(backup_path) else []
        }
        
        with open(os.path.join(backup_path, "_backup_info.json"), 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        # 压缩备份
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zf.write(file_path, arcname)
        
        # 删除未压缩的备份目录
        shutil.rmtree(backup_path)
        
        logger.info(f"[Backup] Created: {zip_path}")
        return zip_path
    
    def restore_backup(self, backup_name: str) -> bool:
        """恢复备份"""
        zip_path = os.path.join(self.backup_dir, f"{backup_name}.zip")
        
        if not os.path.exists(zip_path):
            logger.error(f"[Backup] Not found: {zip_path}")
            return False
        
        # 解压备份
        temp_dir = os.path.join(self.backup_dir, "_temp_restore")
        os.makedirs(temp_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(temp_dir)
        
        # 恢复数据文件
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        
        extracted_dir = os.path.join(temp_dir, backup_name)
        if os.path.exists(extracted_dir):
            for filename in os.listdir(extracted_dir):
                if filename.startswith("_"):
                    continue
                src = os.path.join(extracted_dir, filename)
                dst = os.path.join(self.data_dir, filename)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        logger.info(f"[Backup] Restored: {backup_name}")
        return True
    
    def list_backups(self) -> List[Dict]:
        """列出所有备份"""
        backups = []
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.zip'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    "name": filename[:-4],
                    "size_mb": round(stat.st_size / 1024 / 1024, 2),
                    "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_days: int = 30):
        """清理旧备份"""
        cutoff = datetime.now() - timedelta(days=keep_days)
        
        for backup in self.list_backups():
            created = datetime.fromisoformat(backup['created_at'])
            if created < cutoff:
                filepath = os.path.join(self.backup_dir, f"{backup['name']}.zip")
                os.remove(filepath)
                logger.info(f"[Backup] Removed old backup: {backup['name']}")
