# gateway/router.py
from fastapi import APIRouter, HTTPException
from models.schemas import StudentProfile, RecommendationResponse
from services.rule_engine import RuleEngine
from services.collaborative_filter import CollaborativeFilter
from services.deepseek_agent import DeepSeekAgent
from services.result_merger import ResultMerger

recommendation_router = APIRouter()

# 单例服务实例 - 避免每次请求重复初始化
_rule_engine = RuleEngine()
_collaborative_filter = CollaborativeFilter()
_deepseek_agent = DeepSeekAgent()
_result_merger = ResultMerger()


@recommendation_router.post("/recommend", response_model=RecommendationResponse)
async def recommend(student: StudentProfile):
    """主推荐接口"""
    try:
        # Step 1: Rule Engine - 初筛候选集
        candidates = _rule_engine.filter_candidates(student)

        # Step 2: Collaborative Filter - 群体智能
        cf_scores = _collaborative_filter.get_similarity_scores(student, candidates)

        # Step 3: DeepSeek Agent - 个性化分析
        deepseek_scores = _deepseek_agent.analyze_candidates(student, candidates)

        # Step 4: Result Merger - 综合排序
        recommendations = _result_merger.merge_and_rank(
            candidates, cf_scores, deepseek_scores, student
        )

        return RecommendationResponse(
            student_profile=student,
            recommendations=recommendations,
            generated_at="2024-06-11T10:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))