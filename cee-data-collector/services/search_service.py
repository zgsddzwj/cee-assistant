# services/search_service.py
"""院校搜索服务 - 支持多维度搜索和筛选

支持：
1. 按名称搜索
2. 按省份筛选
3. 按层次筛选
4. 按分数范围筛选
5. 组合筛选
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re

class SortField(Enum):
    SCORE = "score"
    NAME = "name"
    TIER = "tier"
    PLAN_COUNT = "plan_count"

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"

@dataclass
class SearchCriteria:
    """搜索条件"""
    keyword: Optional[str] = None
    province: Optional[str] = None
    tier: Optional[int] = None
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    category: Optional[str] = None
    is_hot: Optional[bool] = None
    sort_by: SortField = SortField.SCORE
    sort_order: SortOrder = SortOrder.DESC
    limit: int = 50
    offset: int = 0

class UniversitySearchService:
    """院校搜索服务"""
    
    def __init__(self, universities: List[Dict] = None):
        self.universities = universities or []
    
    def search(self, criteria: SearchCriteria) -> Dict[str, Any]:
        """执行搜索"""
        results = self.universities.copy()
        
        # 关键词搜索（名称模糊匹配）
        if criteria.keyword:
            results = self._filter_by_keyword(results, criteria.keyword)
        
        # 省份筛选
        if criteria.province:
            results = [u for u in results if u.get('province') == criteria.province]
        
        # 层次筛选
        if criteria.tier:
            results = [u for u in results if u.get('tier') == criteria.tier]
        
        # 分数范围筛选
        if criteria.min_score is not None or criteria.max_score is not None:
            results = self._filter_by_score_range(
                results, 
                criteria.min_score, 
                criteria.max_score
            )
        
        # 专业类别筛选
        if criteria.category:
            results = self._filter_by_category(results, criteria.category)
        
        # 热门筛选
        if criteria.is_hot is not None:
            results = self._filter_by_hot(results, criteria.is_hot)
        
        # 排序
        results = self._sort_results(results, criteria.sort_by, criteria.sort_order)
        
        # 分页
        total = len(results)
        paginated = results[criteria.offset:criteria.offset + criteria.limit]
        
        return {
            "total": total,
            "offset": criteria.offset,
            "limit": criteria.limit,
            "results": paginated
        }
    
    def _filter_by_keyword(self, universities: List[Dict], keyword: str) -> List[Dict]:
        """按关键词过滤"""
        pattern = re.compile(keyword, re.IGNORECASE)
        return [
            u for u in universities 
            if pattern.search(u.get('university_name', ''))
        ]
    
    def _filter_by_score_range(self, universities: List[Dict], min_score: Optional[int], max_score: Optional[int]) -> List[Dict]:
        """按分数范围过滤"""
        filtered = []
        for uni in universities:
            majors = uni.get('majors', [])
            matching_majors = []
            
            for major in majors:
                score = major.get('admission_score', 0)
                if (min_score is None or score >= min_score) and \
                   (max_score is None or score <= max_score):
                    matching_majors.append(major)
            
            if matching_majors:
                uni_copy = uni.copy()
                uni_copy['majors'] = matching_majors
                filtered.append(uni_copy)
        
        return filtered
    
    def _filter_by_category(self, universities: List[Dict], category: str) -> List[Dict]:
        """按专业类别过滤"""
        filtered = []
        for uni in universities:
            majors = [m for m in uni.get('majors', []) if m.get('category') == category]
            if majors:
                uni_copy = uni.copy()
                uni_copy['majors'] = majors
                filtered.append(uni_copy)
        return filtered
    
    def _filter_by_hot(self, universities: List[Dict], is_hot: bool) -> List[Dict]:
        """按热门状态过滤"""
        filtered = []
        for uni in universities:
            majors = [m for m in uni.get('majors', []) if m.get('hot') == is_hot]
            if majors:
                uni_copy = uni.copy()
                uni_copy['majors'] = majors
                filtered.append(uni_copy)
        return filtered
    
    def _sort_results(self, universities: List[Dict], sort_by: SortField, order: SortOrder) -> List[Dict]:
        """排序结果"""
        reverse = order == SortOrder.DESC
        
        if sort_by == SortField.SCORE:
            return sorted(universities, key=lambda u: u.get('majors', [{}])[0].get('admission_score', 0), reverse=reverse)
        elif sort_by == SortField.NAME:
            return sorted(universities, key=lambda u: u.get('university_name', ''), reverse=reverse)
        elif sort_by == SortField.TIER:
            return sorted(universities, key=lambda u: u.get('tier', 3), reverse=reverse)
        elif sort_by == SortField.PLAN_COUNT:
            return sorted(universities, key=lambda u: u.get('total_plan', 0), reverse=reverse)
        
        return universities
    
    def get_provinces(self) -> List[str]:
        """获取所有省份列表"""
        return sorted(set(u.get('province', '') for u in self.universities))
    
    def get_categories(self) -> List[str]:
        """获取所有专业类别"""
        categories = set()
        for uni in self.universities:
            for major in uni.get('majors', []):
                categories.add(major.get('category', ''))
        return sorted(categories)
    
    def get_score_range(self) -> Dict[str, int]:
        """获取分数范围"""
        scores = []
        for uni in self.universities:
            for major in uni.get('majors', []):
                score = major.get('admission_score')
                if score is not None:
                    scores.append(score)
        
        return {
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 750
        }
