# services/collaborative_filter.py
from typing import List, Dict
from models.schemas import StudentProfile, MajorInfo


class CollaborativeFilter:
    """协同过滤服务 - 基于相似考生的选择模式推荐"""
    
    def __init__(self):
        self.historical_choices = self._load_historical_data()
    
    def _load_historical_data(self) -> List[Dict]:
        """加载历史考生选择数据（模拟）"""
        return [
            {"score": 610, "rank": 12000, "province": "北京", "choices": ["080901", "080902"]},
            {"score": 605, "rank": 13500, "province": "北京", "choices": ["080902", "020101"]},
            {"score": 595, "rank": 16000, "province": "北京", "choices": ["020101", "030101"]},
            {"score": 600, "rank": 14000, "province": "北京", "choices": ["070101", "080901"]},
            {"score": 590, "rank": 15500, "province": "北京", "choices": ["030101", "050101"]},
        ]
    
    def get_similarity_scores(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        """计算候选专业与相似考生选择的匹配度"""
        scores = {}
        for candidate in candidates:
            score = self._calculate_similarity_score(student, candidate)
            scores[candidate.code] = score
        return scores
    
    def _calculate_similarity_score(self, student: StudentProfile, candidate: MajorInfo) -> float:
        """计算单个候选专业的协同过滤得分"""
        similarity_scores = []
        
        for historical in self.historical_choices:
            similarity = self._calculate_student_similarity(student, historical)
            if candidate.code in historical["choices"]:
                similarity_scores.append(similarity * 100)
        
        if not similarity_scores:
            return 50.0
        
        return sum(similarity_scores) / len(similarity_scores)
    
    def _calculate_student_similarity(self, student: StudentProfile, historical: Dict) -> float:
        """计算两个考生的相似度 (0-1)"""
        score_diff = abs(student.score - historical["score"])
        score_sim = max(0, 1 - score_diff / 50)
        
        rank_diff = abs(student.rank - historical["rank"])
        rank_sim = max(0, 1 - rank_diff / 5000)
        
        location_sim = 1.0 if student.province == historical["province"] else 0.5
        
        return (score_sim * 0.4 + rank_sim * 0.4 + location_sim * 0.2)