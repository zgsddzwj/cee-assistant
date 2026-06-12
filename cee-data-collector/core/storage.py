# core/storage.py
from typing import Optional, Dict, Any, List
import json
import os
from datetime import datetime

class StorageManager:
    """分级存储管理器 - 管理热数据、核心数据、冷数据的存储
    
    支持三种存储模式：
    1. Redis - 热缓存（高频查询数据）
    2. PostgreSQL - 核心数据（结构化数据）
    3. MinIO - 冷存储（大文件、备份）
    4. 本地JSON - Fallback（无外部存储时使用）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, data_dir: str = './data'):
        self.config = config or {}
        self.data_dir = data_dir
        self.redis_client = None
        self.postgres_client = None
        self.minio_client = None
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 尝试连接外部存储
        self._connect_redis()
        self._connect_postgres()
        self._connect_minio()
    
    def _connect_redis(self):
        """尝试连接Redis"""
        try:
            import redis
            redis_url = self.config.get('redis_url', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            print("[Storage] Redis connected")
        except Exception as e:
            print(f"[Storage] Redis not available: {e}")
            self.redis_client = None
    
    def _connect_postgres(self):
        """尝试连接PostgreSQL"""
        try:
            import psycopg2
            db_url = self.config.get('database_url', 'postgresql://user:pass@localhost/cee')
            self.postgres_client = psycopg2.connect(db_url)
            print("[Storage] PostgreSQL connected")
        except Exception as e:
            print(f"[Storage] PostgreSQL not available: {e}")
            self.postgres_client = None
    
    def _connect_minio(self):
        """尝试连接MinIO"""
        try:
            from minio import Minio
            endpoint = self.config.get('minio_endpoint', 'localhost:9000')
            access_key = self.config.get('minio_access_key', 'minioadmin')
            secret_key = self.config.get('minio_secret_key', 'minioadmin')
            self.minio_client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
            print("[Storage] MinIO connected")
        except Exception as e:
            print(f"[Storage] MinIO not available: {e}")
            self.minio_client = None
    
    def store_hot_data(self, key: str, data: Dict[str, Any], ttl: int = 3600) -> bool:
        """存储热数据到Redis缓存"""
        if self.redis_client is None:
            return False
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            self.redis_client.setex(key, ttl, json_data)
            return True
        except Exception as e:
            print(f"Error storing hot data: {e}")
            return False
    
    def store_core_data(self, table: str, data: Dict[str, Any]) -> bool:
        """存储核心数据到PostgreSQL"""
        if self.postgres_client is None:
            return False
        try:
            # 简化的实现，实际应该使用ORM或参数化查询
            cursor = self.postgres_client.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, list(data.values()))
            self.postgres_client.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error storing core data: {e}")
            return False
    
    def store_cold_data(self, bucket: str, object_key: str, data: bytes) -> bool:
        """存储冷数据到MinIO"""
        if self.minio_client is None:
            return False
        try:
            from io import BytesIO
            self.minio_client.put_object(bucket, object_key, BytesIO(data), len(data))
            return True
        except Exception as e:
            print(f"Error storing cold data: {e}")
            return False
    
    def retrieve_hot_data(self, key: str) -> Optional[Dict[str, Any]]:
        """从Redis缓存获取热数据"""
        if self.redis_client is None:
            return None
        try:
            json_data = self.redis_client.get(key)
            return json.loads(json_data) if json_data else None
        except Exception as e:
            print(f"Error retrieving hot data: {e}")
            return None
    
    # === 本地JSON Fallback 存储 ===
    
    def save_to_json(self, data: Any, filename: str) -> str:
        """保存数据到本地JSON文件"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath
    
    def load_from_json(self, filename: str) -> Any:
        """从本地JSON文件加载数据"""
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_json_files(self) -> List[str]:
        """列出所有JSON数据文件"""
        if not os.path.exists(self.data_dir):
            return []
        return [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
    
    def save_score_data(self, province: str, year: int, data: List[Dict]) -> str:
        """保存分数线数据"""
        filename = f"scores_{province}_{year}.json"
        return self.save_to_json(data, filename)
    
    def save_rank_data(self, province: str, year: int, data: List[Dict]) -> str:
        """保存一分一段表数据"""
        filename = f"ranks_{province}_{year}.json"
        return self.save_to_json(data, filename)
    
    def save_university_data(self, uni_key: str, year: int, data: Dict) -> str:
        """保存院校数据"""
        filename = f"university_{uni_key}_{year}.json"
        return self.save_to_json(data, filename)
    
    def load_score_data(self, province: str, year: int) -> Optional[List[Dict]]:
        """加载分数线数据"""
        filename = f"scores_{province}_{year}.json"
        return self.load_from_json(filename)
    
    def load_rank_data(self, province: str, year: int) -> Optional[List[Dict]]:
        """加载一分一段表数据"""
        filename = f"ranks_{province}_{year}.json"
        return self.load_from_json(filename)
    
    def load_university_data(self, uni_key: str, year: int) -> Optional[Dict]:
        """加载院校数据"""
        filename = f"university_{uni_key}_{year}.json"
        return self.load_from_json(filename)
    
    def get_storage_status(self) -> Dict[str, bool]:
        """获取存储系统状态"""
        return {
            'redis': self.redis_client is not None,
            'postgres': self.postgres_client is not None,
            'minio': self.minio_client is not None,
            'local_json': True,  # 总是可用
        }
