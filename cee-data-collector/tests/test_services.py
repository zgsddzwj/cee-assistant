# tests/test_services.py
"""服务层单元测试"""

import pytest
from services.search_service import UniversitySearchService, SearchCriteria
from services.recommendation_service import RecommendationService
from services.analytics_service import AnalyticsService

class TestSearchService:
    """测试搜索服务"""
    
    @pytest.fixture
    def sample_universities(self):
        return [
            {
                "university_name": "清华大学",
                "province": "北京",
                "tier": 1,
                "majors": [
                    {"name": "计算机", "admission_score": 680, "category": "工学", "hot": True},
                    {"name": "数学", "admission_score": 670, "category": "理学", "hot": False}
                ]
            },
            {
                "university_name": "北京大学",
                "province": "北京",
                "tier": 1,
                "majors": [
                    {"name": "金融", "admission_score": 675, "category": "经济学", "hot": True}
                ]
            },
            {
                "university_name": "复旦大学",
                "province": "上海",
                "tier": 1,
                "majors": [
                    {"name": "计算机", "admission_score": 665, "category": "工学", "hot": True}
                ]
            }
        ]
    
    def test_search_by_keyword(self, sample_universities):
        service = UniversitySearchService(sample_universities)
        criteria = SearchCriteria(keyword="清华")
        result = service.search(criteria)
        
        assert result["total"] == 1
        assert result["results"][0]["university_name"] == "清华大学"
    
    def test_search_by_province(self, sample_universities):
        service = UniversitySearchService(sample_universities)
        criteria = SearchCriteria(province="北京")
        result = service.search(criteria)
        
        assert result["total"] == 2
    
    def test_search_by_score_range(self, sample_universities):
        service = UniversitySearchService(sample_universities)
        criteria = SearchCriteria(min_score=670, max_score=680)
        result = service.search(criteria)
        
        assert result["total"] > 0

class TestRecommendationService:
    """测试推荐服务"""
    
    @pytest.fixture
    def sample_universities(self):
        return [
            {
                "university_name": "清华大学",
                "province": "北京",
                "tier": 1,
                "majors": [
                    {"name": "计算机", "admission_score": 680, "category": "工学", "hot": True}
                ]
            }
        ]
    
    def test_recommend(self, sample_universities):
        service = RecommendationService(sample_universities)
        results = service.recommend(
            score=690,
            rank=1000,
            province="北京",
            subject_type="综合",
            interests=["计算机"]
        )
        
        assert len(results) > 0
        assert results[0].match_score > 0

class TestAnalyticsService:
    """测试分析服务"""
    
    @pytest.fixture
    def sample_scores(self):
        return [
            {"province": "beijing", "year": 2022, "batch": "本科一批", "score": 580, "subject_type": "综合"},
            {"province": "beijing", "year": 2023, "batch": "本科一批", "score": 585, "subject_type": "综合"},
            {"province": "beijing", "year": 2024, "batch": "本科一批", "score": 590, "subject_type": "综合"}
        ]
    
    def test_analyze_score_trend(self, sample_scores):
        service = AnalyticsService(scores=sample_scores)
        result = service.analyze_score_trend("beijing", "本科一批", [2022, 2023, 2024])
        
        assert result["trend"] == "上升"
        assert len(result["data"]) == 3
