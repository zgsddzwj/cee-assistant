# core/cache_manager.py
"""缓存管理器 - 提供多级缓存支持

特性：
1. 内存缓存（LRU）- 最热数据
2. Redis 缓存 - 分布式缓存
3. 本地文件缓存 - 持久化缓存
4. 缓存预热和自动刷新
"""

import json
import os
import time
import pickle
import hashlib
from typing import Dict, Any, Optional, List, Callable
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """多级缓存管理器"""
    
    def __init__(self, data_dir: str = './data/cache', redis_client=None, max_memory_size: int = 128):
        self.data_dir = data_dir
        self.redis = redis_client
        self.max_memory_size = max_memory_size
        self._memory_cache: Dict[str, Any] = {}
        self._cache_metadata: Dict[str, Dict] = {}  # 存储过期时间等元数据
        
        os.makedirs(data_dir, exist_ok=True)
        
        logger.info(f"[CacheManager] Initialized with memory_size={max_memory_size}, data_dir={data_dir}")
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存键"""
        key_data = f"{prefix}:{args}:{kwargs}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_file_path(self, key: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.data_dir, f"{key}.cache")
    
    def _is_expired(self, key: str) -> bool:
        """检查缓存是否过期"""
        if key not in self._cache_metadata:
            return True
        
        metadata = self._cache_metadata[key]
        if 'expires_at' in metadata and time.time() > metadata['expires_at']:
            return True
        
        return False
    
    def get(self, key: str, default=None) -> Any:
        """获取缓存值（多级缓存）"""
        # 1. 检查内存缓存
        if key in self._memory_cache and not self._is_expired(key):
            logger.debug(f"[Cache] Memory hit: {key}")
            return self._memory_cache[key]
        
        # 2. 检查 Redis 缓存
        if self.redis:
            try:
                value = self.redis.get(key)
                if value:
                    logger.debug(f"[Cache] Redis hit: {key}")
                    data = json.loads(value)
                    # 回填内存缓存
                    self._memory_cache[key] = data
                    return data
            except Exception as e:
                logger.warning(f"[Cache] Redis error: {e}")
        
        # 3. 检查文件缓存
        file_path = self._get_file_path(key)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                
                # 检查文件缓存是否过期
                if not self._is_expired(key):
                    logger.debug(f"[Cache] File hit: {key}")
                    # 回填内存缓存
                    self._memory_cache[key] = data
                    return data
            except Exception as e:
                logger.warning(f"[Cache] File cache error: {e}")
        
        return default
    
    def set(self, key: str, value: Any, ttl: int = 3600, persist: bool = False) -> bool:
        """设置缓存值（多级缓存）"""
        try:
            # 1. 存储到内存
            self._memory_cache[key] = value
            
            # 2. 存储到 Redis
            if self.redis:
                try:
                    json_value = json.dumps(value, ensure_ascii=False)
                    self.redis.setex(key, ttl, json_value)
                except Exception as e:
                    logger.warning(f"[Cache] Redis set error: {e}")
            
            # 3. 如果需要持久化，存储到文件
            if persist:
                file_path = self._get_file_path(key)
                with open(file_path, 'wb') as f:
                    pickle.dump(value, f)
            
            # 更新元数据
            self._cache_metadata[key] = {
                'created_at': time.time(),
                'expires_at': time.time() + ttl,
                'ttl': ttl,
                'persist': persist,
            }
            
            # 清理内存缓存（如果过大）
            self._cleanup_memory_cache()
            
            return True
            
        except Exception as e:
            logger.error(f"[Cache] Set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        # 删除内存缓存
        self._memory_cache.pop(key, None)
        self._cache_metadata.pop(key, None)
        
        # 删除 Redis 缓存
        if self.redis:
            try:
                self.redis.delete(key)
            except Exception as e:
                logger.warning(f"[Cache] Redis delete error: {e}")
        
        # 删除文件缓存
        file_path = self._get_file_path(key)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return True
    
    def clear(self):
        """清空所有缓存"""
        self._memory_cache.clear()
        self._cache_metadata.clear()
        
        if self.redis:
            try:
                # 只删除当前应用的缓存键
                for key in list(self._cache_metadata.keys()):
                    self.redis.delete(key)
            except Exception as e:
                logger.warning(f"[Cache] Redis clear error: {e}")
        
        # 清空文件缓存目录
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.cache'):
                os.remove(os.path.join(self.data_dir, filename))
        
        logger.info("[Cache] All caches cleared")
    
    def _cleanup_memory_cache(self):
        """清理内存缓存（LRU策略）"""
        if len(self._memory_cache) > self.max_memory_size:
            # 移除最旧的条目
            sorted_keys = sorted(
                self._cache_metadata.keys(),
                key=lambda k: self._cache_metadata[k].get('created_at', 0)
            )
            
            keys_to_remove = sorted_keys[:len(sorted_keys) - self.max_memory_size]
            for key in keys_to_remove:
                self._memory_cache.pop(key, None)
                # 保留元数据以便知道是否有过期时间
    
    def cached(self, ttl: int = 3600, persist: bool = False):
        """缓存装饰器"""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                # 生成缓存键
                key = self._generate_key(func.__name__, *args, **kwargs)
                
                # 尝试获取缓存
                cached_value = self.get(key)
                if cached_value is not None:
                    return cached_value
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 存储缓存
                self.set(key, result, ttl, persist)
                
                return result
            
            return wrapper
        return decorator
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            'memory_cache_size': len(self._memory_cache),
            'memory_cache_limit': self.max_memory_size,
            'metadata_count': len(self._cache_metadata),
            'file_cache_files': len([f for f in os.listdir(self.data_dir) if f.endswith('.cache')]),
            'redis_connected': self.redis is not None,
        }


# 全局缓存实例
cache = CacheManager()
