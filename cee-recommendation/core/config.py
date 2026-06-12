# core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class RecommendationConfig(BaseSettings):
    """推荐引擎配置管理"""
    deepseek_api_key: Optional[str] = None
    deepseek_api_base: str = "https://api.deepseek.com/v1"
    redis_url: str = "redis://localhost:6379"
    database_url: str = "postgresql://user:pass@localhost/cee"
    
    class Config:
        env_file = ".env"
        env_prefix = "CEE_"