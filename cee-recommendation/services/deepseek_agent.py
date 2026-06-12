# services/deepseek_agent.py
from typing import List, Dict
from models.schemas import StudentProfile, MajorInfo, Category
import os


class DeepSeekAgent:
    """DeepSeek Agent 服务 - 生成个性化推荐理由"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.mock_mode = self.api_key is None
    
    def analyze_candidates(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        """分析候选专业并返回评分"""
        if self.mock_mode:
            return self._mock_analyze(student, candidates)
        return self._call_deepseek_api(student, candidates)
    
    def _mock_analyze(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        """模拟分析（开发阶段使用）"""
        scores = {}
        for candidate in candidates:
            score = self._calculate_mock_score(student, candidate)
            scores[candidate.code] = score
        return scores
    
    def _calculate_mock_score(self, student: StudentProfile, candidate: MajorInfo) -> float:
        """基于规则的模拟评分"""
        score = 50.0
        
        interest_keywords = {
            "计算机科学与技术": ["编程", "计算机", "软件", "技术"],
            "软件工程": ["编程", "软件", "开发"],
            "经济学": ["经济", "金融", "商业"],
            "法学": ["法律", "正义", "辩论"],
            "临床医学": ["医学", "医生", "健康"],
            "数学与应用数学": ["数学", "逻辑", "理论"],
        }
        
        keywords = interest_keywords.get(candidate.name, [])
        for interest in student.interests:
            if any(kw in interest for kw in keywords):
                score += 20
                break
        
        career_keywords = {
            "计算机科学与技术": ["工程师", "程序员", "技术"],
            "软件工程": ["工程师", "程序员", "开发"],
            "经济学": ["分析师", "金融", "投资"],
            "临床医学": ["医生", "医师", "医疗"],
        }
        
        if student.career_plan:
            career_kws = career_keywords.get(candidate.name, [])
            for kw in career_kws:
                if kw in student.career_plan:
                    score += 15
                    break
        
        return min(100, score)
    
    def _call_deepseek_api(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        """调用 DeepSeek API 进行分析"""
        # TODO: 实现实际的 API 调用
        return self._mock_analyze(student, candidates)
    
    def generate_recommendation_reason(self, student: StudentProfile, candidate: MajorInfo, category: Category) -> str:
        """生成个性化推荐理由"""
        if self.mock_mode:
            return self._mock_generate_reason(student, candidate, category)
        return self._mock_generate_reason(student, candidate, category)
    
    def _mock_generate_reason(self, student: StudentProfile, candidate: MajorInfo, category: Category) -> str:
        """生成模拟推荐理由"""
        reasons = {
            Category.CHONG: f"您的分数接近{candidate.name}的录取线，有一定挑战性。",
            Category.WEN: f"您的分数与{candidate.name}的录取线匹配度较高，建议重点考虑。",
            Category.BAO: f"您的分数高于{candidate.name}的录取线，录取概率较大。",
        }
        
        base_reason = reasons.get(category, "")
        
        if student.interests:
            base_reason += f" 您的兴趣{'、'.join(student.interests)}与该专业培养方向有一定关联。"
        
        return base_reason