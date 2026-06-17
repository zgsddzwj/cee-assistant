# utils/data_loader.py
"""数据加载器 - 高效加载和查询数据

特性：
1. 懒加载（按需加载）
2. 数据索引（快速查询）
3. 批量加载
4. 内存优化
"""

import json
import os
from typing import Dict, List, Any, Optional, Iterator, Callable
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class DataLoader:
    """高效数据加载器"""
    
    def __init__(self, data_dir: str = './data'):
        self.data_dir = data_dir
        self._cache: Dict[str, Any] = {}
        self._indexes: Dict[str, Dict[str, List[int]]] = {}  # 索引结构
        
        logger.info(f"[DataLoader] Initialized with data_dir={data_dir}")
    
    def _get_file_path(self, filename: str) -> str:
        """获取文件路径"""
        return os.path.join(self.data_dir, filename)
    
    def load_json(self, filename: str) -> Any:
        """加载JSON文件（带缓存）"""
        if filename in self._cache:
            return self._cache[filename]
        
        filepath = self._get_file_path(filename)
        if not os.path.exists(filepath):
            logger.warning(f"[DataLoader] File not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._cache[filename] = data
            logger.info(f"[DataLoader] Loaded {filename} ({len(str(data))} bytes)")
            return data
            
        except Exception as e:
            logger.error(f"[DataLoader] Error loading {filename}: {e}")
            return None
    
    def load_json_lines(self, filename: str) -> Iterator[Dict]:
        """逐行加载JSON文件（内存友好）"""
        filepath = self._get_file_path(filename)
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if filename.endswith('.jsonl'):
                    for line in f:
                        yield json.loads(line)
                else:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            yield item
                    else:
                        yield data
        except Exception as e:
            logger.error(f"[DataLoader] Error loading {filename}: {e}")
    
    def build_index(self, filename: str, field: str) -> Dict[str, List[int]]:
        """为数据文件构建索引"""
        data = self.load_json(filename)
        if not data or not isinstance(data, list):
            return {}
        
        index: Dict[str, List[int]] = {}
        for i, item in enumerate(data):
            key = str(item.get(field, ''))
            if key not in index:
                index[key] = []
            index[key].append(i)
        
        index_key = f"{filename}:{field}"
        self._indexes[index_key] = index
        
        logger.info(f"[DataLoader] Built index for {filename}.{field} ({len(index)} keys)")
        return index
    
    def query_by_field(self, filename: str, field: str, value: str) -> List[Dict]:
        """根据字段值查询数据"""
        data = self.load_json(filename)
        if not data or not isinstance(data, list):
            return []
        
        # 检查是否有索引
        index_key = f"{filename}:{field}"
        if index_key in self._indexes:
            index = self._indexes[index_key]
            indices = index.get(str(value), [])
            return [data[i] for i in indices]
        
        # 线性搜索
        return [item for item in data if str(item.get(field, '')) == str(value)]
    
    def query_range(self, filename: str, field: str, min_val: Any, max_val: Any) -> List[Dict]:
        """范围查询"""
        data = self.load_json(filename)
        if not data or not isinstance(data, list):
            return []
        
        results = []
        for item in data:
            value = item.get(field)
            if value is not None and min_val <= value <= max_val:
                results.append(item)
        
        return results
    
    def filter_data(self, filename: str, predicate: Callable[[Dict], bool]) -> List[Dict]:
        """使用自定义条件过滤数据"""
        data = self.load_json(filename)
        if not data or not isinstance(data, list):
            return []
        
        return [item for item in data if predicate(item)]
    
    def batch_load(self, filenames: List[str]) -> Dict[str, Any]:
        """批量加载多个文件"""
        results = {}
        for filename in filenames:
            results[filename] = self.load_json(filename)
        return results
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        self._indexes.clear()
        logger.info("[DataLoader] Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return {
            'cached_files': len(self._cache),
            'indexes': len(self._indexes),
            'cache_size_mb': sum(len(str(v)) for v in self._cache.values()) / 1024 / 1024,
        }


class LazyDataLoader:
    """懒加载数据加载器"""
    
    def __init__(self, data_dir: str = './data'):
        self.data_dir = data_dir
        self._loaded_files: set = set()
    
    def load(self, filename: str) -> Any:
        """懒加载文件"""
        if filename in self._loaded_files:
            return None  # 已经加载过
        
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._loaded_files.add(filename)
            return data
        except Exception as e:
            logger.error(f"[LazyDataLoader] Error loading {filename}: {e}")
            return None
    
    def is_loaded(self, filename: str) -> bool:
        """检查文件是否已加载"""
        return filename in self._loaded_files


# 便捷函数
@lru_cache(maxsize=32)
def load_score_data(province: str, year: int, data_dir: str = './data') -> List[Dict]:
    """加载分数线数据（带缓存）"""
    loader = DataLoader(data_dir)
    filename = f"scores_{province}_{year}.json"
    return loader.load_json(filename) or []

@lru_cache(maxsize=32)
def load_university_data(uni_key: str, year: int, data_dir: str = './data') -> Optional[Dict]:
    """加载院校数据（带缓存）"""
    loader = DataLoader(data_dir)
    filename = f"university_{uni_key}_{year}.json"
    return loader.load_json(filename)
