# services/recommendation_service.py
"""专业推荐服务 - 基于多维度匹配算法

支持：
1. 分数匹配
2. 兴趣匹配
3. 职业规划匹配
4. 地域偏好匹配
5. 综合推荐排序
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import random

class RecommendationType(str, Enum):
    CHONG = "冲"  # 冲刺院校
    WEN = "稳"    # 稳妥院校
    BAO = "保"    # 保底院校

@dataclass
class MatchResult:
    """匹配结果"""
    university: Dict
    major: Dict
    match_score: float
    probability: str
    rec_type: RecommendationType
    reasons: List[str]

class RecommendationService:
    """推荐服务"""
    
    def __init__(self, universities: List[Dict] = None):
        self.universities = universities or []
    
    def recommend(self, score: int, rank: Optional[int], province: str, 
                  subject_type: str, interests: Optional[List[str]] = None,
                  career_plan: Optional[str] = None,
                  preferred_provinces: Optional[List[str]] = None) -> List[MatchResult]:
        """生成推荐列表"""
        results = []
        
        for uni in self.universities:
            for major in uni.get('majors', []):
                match_result = self._calculate_match(
                    score, rank, province, subject_type,
                    uni, major, interests, career_plan, preferred_provinces
                )
                
                if match_result:
                    results.append(match_result)
        
        # 按匹配分数排序
        results.sort(key=lambda x: x.match_score, reverse=True)
        
        return results[:50]  # 返回前50个推荐
    
    def _calculate_match(self, score: int, rank: Optional[int], province: str,
                         subject_type: str, university: Dict, major: Dict,
                         interests: Optional[List[str]], career_plan: Optional[str],
                         preferred_provinces: Optional[List[str]]) -> Optional[MatchResult]:
        """计算匹配度"""
        admission_score = major.get('admission_score', 0)
        
        # 分数差距
        score_diff = score - admission_score
        
        # 确定推荐类型
        if score_diff >= -10 and score_diff <= 5:
            rec_type = RecommendationType.CHONG
            probability = "60-80%"
        elif score_diff > 5 and score_diff <= 30:
            rec_type = RecommendationType.WEN
            probability = "80-95%"
        elif score_diff > 30:
            rec_type = RecommendationType.BAO
            probability = "95%+"
        else:
            return None  # 分数差距太大，不推荐
        
        # 计算匹配分数 (0-100)
        match_score = 0.0
        reasons = []
        
        # 1. 分数匹配 (40分)
        if score_diff >= 0:
            match_score += 40
            reasons.append(f"分数高于录取线{score_diff}分")
        elif score_diff >= -10:
            match_score += 30
            reasons.append(f"分数接近录取线，可冲刺")
        
        # 2. 兴趣匹配 (20分)
        if interests:
            major_name = major.get('name', '')
            for interest in interests:
                if interest in major_name or interest in major.get('category', ''):
                    match_score += 20
                    reasons.append(f"符合兴趣方向：{interest}")
                    break
        
        # 3. 地域匹配 (20分)
        if preferred_provinces:
            uni_province = university.get('province', '')
            if uni_province in preferred_provinces:
                match_score += 20
                reasons.append(f"位于意向省份：{uni_province}")
        
        # 4. 院校层次 (20分)
        tier = university.get('tier', 3)
        if tier == 1:
            match_score += 20
            reasons.append("985/211/双一流院校")
        elif tier == 2:
            match_score += 15
            reasons.append("省重点院校")
        
        # 5. 热门专业加分
        if major.get('hot'):
            match_score += 5
            reasons.append("热门专业")
        
        return MatchResult(
            university=university,
            major=major,
            match_score=min(match_score, 100),
            probability=probability,
            rec_type=rec_type,
            reasons=reasons
        )
    
    def get_recommendation_summary(self, results: List[MatchResult]) -> Dict[str, Any]:
        """获取推荐汇总"""
        chong_count = len([r for r in results if r.rec_type == RecommendationType.CHONG])
        wen_count = len([r for r in results if r.rec_type == RecommendationType.WEN])
        bao_count = len([r for r in results if r.rec_type == RecommendationType.BAO])
        
        return {
            "total": len(results),
            "chong": chong_count,
            "wen": wen_count,
            "bao": bao_count,
            "avg_score": sum(r.match_score for r in results) / len(results) if results else 0
        }
