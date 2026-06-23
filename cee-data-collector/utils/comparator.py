# utils/comparator.py
"""数据比对器 - 比较不同版本的数据差异

支持：
1. 分数线变化比对
2. 院校招生人数变化
3. 专业分数变化
4. 生成差异报告
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

class ChangeType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"

@dataclass
class DataDiff:
    """数据差异项"""
    change_type: ChangeType
    key: str
    old_value: Any = None
    new_value: Any = None
    field: Optional[str] = None

class DataComparator:
    """数据比对器"""
    
    def compare_scores(self, old_data: List[Dict], new_data: List[Dict]) -> List[DataDiff]:
        """比对分数线变化"""
        diffs = []
        
        # 建立索引
        old_index = {self._make_key(d): d for d in old_data}
        new_index = {self._make_key(d): d for d in new_data}
        
        # 检查新增和修改
        for key, new_item in new_index.items():
            if key not in old_index:
                diffs.append(DataDiff(ChangeType.ADDED, key, None, new_item))
            else:
                old_item = old_index[key]
                if old_item.get('score') != new_item.get('score'):
                    diffs.append(DataDiff(
                        ChangeType.MODIFIED, key,
                        old_item.get('score'), new_item.get('score'),
                        field='score'
                    ))
        
        # 检查删除
        for key, old_item in old_index.items():
            if key not in new_index:
                diffs.append(DataDiff(ChangeType.REMOVED, key, old_item, None))
        
        return diffs
    
    def _make_key(self, item: Dict) -> str:
        """生成唯一键"""
        return f"{item.get('province', '')}_{item.get('year', '')}_{item.get('batch', '')}_{item.get('subject_type', '')}"
    
    def generate_report(self, diffs: List[DataDiff], title: str = "数据比对报告") -> Dict:
        """生成比对报告"""
        added = [d for d in diffs if d.change_type == ChangeType.ADDED]
        removed = [d for d in diffs if d.change_type == ChangeType.REMOVED]
        modified = [d for d in diffs if d.change_type == ChangeType.MODIFIED]
        
        return {
            "title": title,
            "summary": {
                "total_changes": len(diffs),
                "added": len(added),
                "removed": len(removed),
                "modified": len(modified),
            },
            "details": {
                "added": [{"key": d.key, "value": d.new_value} for d in added],
                "removed": [{"key": d.key, "value": d.old_value} for d in removed],
                "modified": [
                    {
                        "key": d.key,
                        "field": d.field,
                        "old": d.old_value,
                        "new": d.new_value,
                        "change": f"{d.old_value} -> {d.new_value}"
                    }
                    for d in modified
                ]
            }
        }
