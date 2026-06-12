# tests/test_config.py
def test_recommendation_config_loads():
    from core.config import RecommendationConfig
    config = RecommendationConfig()
    assert config.deepseek_api_base == "https://api.deepseek.com/v1"
    assert config.redis_url == "redis://localhost:6379"
    assert config.database_url.startswith("postgresql://")