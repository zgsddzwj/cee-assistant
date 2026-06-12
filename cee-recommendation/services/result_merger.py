# services/result_merger.py
from typing import List, Dict
from models.schemas import StudentProfile, MajorInfo, RecommendationResult, Category
from services.rule_engine import RuleEngine
from services.deepseek_agent import DeepSeekAgent


class ResultMerger:
    """结果融合排序服务 - 综合多源推荐结果"""
    
    RULE_WEIGHT = 0.3
    CF_WEIGHT = 0.2
    DEEPSEEK_WEIGHT = 0.3
    INTEREST_WEIGHT = 0.2
    
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.deepseek_agent = DeepSeekAgent()
    
    def merge_and_rank(
        self,
        candidates: List[MajorInfo],
        cf_scores: Dict[str, float],
        deepseek_scores: Dict[str, float],
        student: StudentProfile
    ) -> List[RecommendationResult]:
        """融合多源结果并排序"""
        results = []
        
        for candidate in candidates:
            rule_score = self.rule_engine.calculate_rule_score(student, candidate)
            cf_score = cf_scores.get(candidate.code, 50)
            deepseek_score = deepseek_scores.get(candidate.code, 50)
            interest_match = self._calculate_interest_match(student, candidate)
            
            final_score = (
                rule_score * self.RULE_WEIGHT +
                cf_score * self.CF_WEIGHT +
                deepseek_score * self.DEEPSEEK_WEIGHT +
                interest_match * 100 * self.INTEREST_WEIGHT
            )
            
            category, probability = self._determine_category(rule_score)
            
            reason = self.deepseek_agent.generate_recommendation_reason(
                student, candidate, category
            )
            
            result = RecommendationResult(
                college=None,
                major=candidate,
                category=category,
                probability=probability,
                score=final_score,
                reason=reason
            )
            results.append(result)
        
        results.sort(key=lambda x: x.score, reverse=True)
        results = self._ensure_distribution(results)
        
        return results
    
    def _calculate_interest_match(self, student: StudentProfile, candidate: MajorInfo) -> float:
        """计算兴趣匹配度 (0-1)"""
        if not student.interests:
            return 0.5
        
        major_interests = {
            "计算机科学与技术": ["编程", "计算机", "软件", "技术", "数学"],
            "软件工程": ["编程", "软件", "开发", "技术"],
            "经济学": ["经济", "金融", "商业", "数学"],
            "法学": ["法律", "正义", "辩论", "社会"],
            "临床医学": ["医学", "医生", "健康", "生物"],
            "数学与应用数学": ["数学", "逻辑", "理论", "研究"],
        }
        
        keywords = major_interests.get(candidate.name, [])
        matches = sum(1 for interest in student.interests if any(kw in interest for kw in keywords))
        
        return min(1.0, matches / max(len(student.interests), 1))
    
    def _determine_category(self, rule_score: float) -> tuple:
        """根据规则得分确定冲稳保类别"""
        if rule_score < 40:
            return Category.CHONG, 0.2
        elif rule_score < 70:
            return Category.WEN, 0.6
        else:
            return Category.BAO, 0.85
    
    def _ensure_distribution(self, results: List[RecommendationResult]) -> List[RecommendationResult]:
        """确保推荐结果有合理的冲稳保分布"""
        chong = [r for r in results if r.category == Category.CHONG]
        wen = [r for r in results if r.category == Category.WEN]
        bao = [r for r in results if r.category == Category.BAO]
        
        total = len(results)
        ideal_chong = max(1, int(total * 0.2))
        ideal_wen = max(1, int(total * 0.5))
        ideal_bao = max(1, int(total * 0.3))
        
        distributed = []
        distributed.extend(chong[:ideal_chong])
        distributed.extend(wen[:ideal_wen])
        distributed.extend(bao[:ideal_bao])
        
        remaining = [r for r in results if r not in distributed]
        distributed.extend(remaining[:total - len(distributed)])
        
        distributed.sort(key=lambda x: x.score, reverse=True)
        
        return distributed