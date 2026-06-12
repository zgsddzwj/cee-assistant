# gateway/router.py
from fastapi import APIRouter, HTTPException
from models.schemas import StudentProfile, RecommendationResponse
from services.rule_engine import RuleEngine
from services.collaborative_filter import CollaborativeFilter
from services.deepseek_agent import DeepSeekAgent
from services.result_merger import ResultMerger

recommendation_router = APIRouter()


@recommendation_router.post("/recommend", response_model=RecommendationResponse)
async def recommend(student: StudentProfile):
    """主推荐接口"""
    try:
        # Step 1: Rule Engine - 初筛候选集
        rule_engine = RuleEngine()
        candidates = rule_engine.filter_candidates(student)
        
        # Step 2: Collaborative Filter - 群体智能
        cf = CollaborativeFilter()
        cf_scores = cf.get_similarity_scores(student, candidates)
        
        # Step 3: DeepSeek Agent - 个性化分析
        agent = DeepSeekAgent()
        deepseek_scores = agent.analyze_candidates(student, candidates)
        
        # Step 4: Result Merger - 综合排序
        merger = ResultMerger()
        recommendations = merger.merge_and_rank(
            candidates, cf_scores, deepseek_scores, student
        )
        
        return RecommendationResponse(
            student_profile=student,
            recommendations=recommendations,
            generated_at="2024-06-11T10:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))