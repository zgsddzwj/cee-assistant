# api/main.py
"""FastAPI 主应用 - 提供 RESTful API 接口

支持：
1. 数据查询 API
2. 搜索 API
3. 推荐 API
4. 分析 API
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os

from models.schemas import QueryRequest, RecommendationResult
from services.search_service import UniversitySearchService, SearchCriteria
from services.recommendation_service import RecommendationService
from services.analytics_service import AnalyticsService

app = FastAPI(
    title="CEE Data Collector API",
    description="高考数据采集与分析 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载数据
def load_data():
    data_dir = './data'
    universities = []
    scores = []
    
    uni_file = os.path.join(data_dir, 'all_universities_2024.json')
    if os.path.exists(uni_file):
        with open(uni_file, 'r', encoding='utf-8') as f:
            universities = json.load(f)
    
    score_file = os.path.join(data_dir, 'all_scores_2024.json')
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = json.load(f)
    
    return universities, scores

universities_data, scores_data = load_data()

@app.get("/")
async def root():
    return {"message": "CEE Data Collector API", "version": "1.0.0"}

@app.get("/universities")
async def get_universities(
    province: Optional[str] = None,
    tier: Optional[int] = None,
    keyword: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0)
):
    """获取院校列表"""
    service = UniversitySearchService(universities_data)
    criteria = SearchCriteria(
        province=province,
        tier=tier,
        keyword=keyword,
        limit=limit,
        offset=offset
    )
    return service.search(criteria)

@app.get("/universities/{uni_id}")
async def get_university(uni_id: str):
    """获取院校详情"""
    for uni in universities_data:
        if uni.get('university_id') == uni_id or uni.get('university_name') == uni_id:
            return uni
    raise HTTPException(status_code=404, detail="University not found")

@app.post("/recommend")
async def recommend(request: QueryRequest):
    """获取志愿推荐"""
    service = RecommendationService(universities_data)
    results = service.recommend(
        score=request.score,
        rank=request.rank,
        province=request.province,
        subject_type=request.subject_type,
        interests=request.interests,
        career_plan=request.career_plan,
        preferred_provinces=request.preferred_provinces
    )
    
    return {
        "total": len(results),
        "summary": service.get_recommendation_summary(results),
        "recommendations": [
            {
                "university": r.university,
                "major": r.major,
                "match_score": r.match_score,
                "probability": r.probability,
                "type": r.rec_type.value,
                "reasons": r.reasons
            }
            for r in results[:20]
        ]
    }

@app.get("/analytics/trend")
async def get_score_trend(
    province: str,
    batch: str,
    years: str = Query(..., description="Comma-separated years, e.g., 2022,2023,2024")
):
    """获取分数线趋势"""
    year_list = [int(y.strip()) for y in years.split(',')]
    service = AnalyticsService(scores=scores_data, universities=universities_data)
    return service.analyze_score_trend(province, batch, year_list)

@app.get("/analytics/difficulty")
async def get_university_difficulty():
    """获取院校难度排名"""
    service = AnalyticsService(universities=universities_data)
    return service.analyze_university_difficulty()

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "data_loaded": len(universities_data) > 0,
        "universities_count": len(universities_data),
        "scores_count": len(scores_data)
    }
