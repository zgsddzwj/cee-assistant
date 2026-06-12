# services/rule_engine.py
from typing import List
from models.schemas import StudentProfile, MajorInfo


class RuleEngine:
    """规则引擎 - 基于分数和位次初筛候选院校"""
    
    SCORE_TOLERANCE = 20
    RANK_TOLERANCE = 0.2
    
    def __init__(self):
        self.mock_colleges = self._load_mock_data()
    
    def _load_mock_data(self) -> List[MajorInfo]:
        """加载模拟数据（开发阶段）"""
        return [
            MajorInfo(code="080901", name="计算机科学与技术", category="工学", admission_score_2023=610, admission_rank_2023=12000),
            MajorInfo(code="080902", name="软件工程", category="工学", admission_score_2023=605, admission_rank_2023=13500),
            MajorInfo(code="020101", name="经济学", category="经济学", admission_score_2023=595, admission_rank_2023=16000),
            MajorInfo(code="030101", name="法学", category="法学", admission_score_2023=590, admission_rank_2023=17500),
            MajorInfo(code="050101", name="汉语言文学", category="文学", admission_score_2023=585, admission_rank_2023=19000),
            MajorInfo(code="070101", name="数学与应用数学", category="理学", admission_score_2023=600, admission_rank_2023=14000),
            MajorInfo(code="100201", name="临床医学", category="医学", admission_score_2023=620, admission_rank_2023=10000),
            MajorInfo(code="120201", name="工商管理", category="管理学", admission_score_2023=580, admission_rank_2023=20000),
        ]
    
    def filter_candidates(self, student: StudentProfile) -> List[MajorInfo]:
        """根据考生分数和位次筛选候选专业"""
        candidates = []
        for major in self.mock_colleges:
            if self._is_match(student, major):
                candidates.append(major)
        return candidates
    
    def _is_match(self, student: StudentProfile, major: MajorInfo) -> bool:
        """判断考生是否符合专业录取条件"""
        if major.admission_score_2023 is None:
            return False
        
        score_match = (
            student.score - self.SCORE_TOLERANCE <= major.admission_score_2023 <=
            student.score + self.SCORE_TOLERANCE
        )
        
        rank_match = True
        if major.admission_rank_2023 is not None:
            rank_lower = major.admission_rank_2023 * (1 - self.RANK_TOLERANCE)
            rank_upper = major.admission_rank_2023 * (1 + self.RANK_TOLERANCE)
            rank_match = rank_lower <= student.rank <= rank_upper
        
        return score_match and rank_match
    
    def calculate_rule_score(self, student: StudentProfile, major: MajorInfo) -> float:
        """计算规则匹配得分 (0-100)"""
        if major.admission_score_2023 is None:
            return 0.0
        
        score_diff = abs(student.score - major.admission_score_2023)
        score_factor = max(0, 1 - score_diff / self.SCORE_TOLERANCE)
        
        rank_factor = 1.0
        if major.admission_rank_2023 is not None:
            rank_diff = abs(student.rank - major.admission_rank_2023)
            rank_factor = max(0, 1 - rank_diff / (major.admission_rank_2023 * self.RANK_TOLERANCE))
        
        return (score_factor * 0.6 + rank_factor * 0.4) * 100