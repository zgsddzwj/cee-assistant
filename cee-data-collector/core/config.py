# core/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import Field

class DataCollectorConfig(BaseSettings):
    """数据采集器配置管理
    
    使用 Pydantic 进行配置验证，支持环境变量覆盖。
    """
    
    # 应用配置
    app_name: str = Field(default="cee-data-collector", description="应用名称")
    debug: bool = Field(default=False, description="调试模式")
    log_level: str = Field(default="INFO", description="日志级别")
    
    # 数据配置
    data_dir: str = Field(default="./data", description="数据存储目录")
    mock_mode: bool = Field(default=True, description="是否使用模拟数据模式")
    default_year: int = Field(default=2024, ge=2010, le=2030, description="默认年份")
    
    # 爬虫配置
    request_timeout: int = Field(default=15, ge=1, le=60, description="请求超时时间(秒)")
    request_delay_min: float = Field(default=2.0, ge=0.1, le=10.0, description="最小请求延迟(秒)")
    request_delay_max: float = Field(default=5.0, ge=0.1, le=30.0, description="最大请求延迟(秒)")
    max_retries: int = Field(default=3, ge=0, le=10, description="最大重试次数")
    
    # Redis 配置
    redis_url: str = Field(default="redis://localhost:6379", description="Redis连接URL")
    redis_ttl: int = Field(default=3600, ge=60, description="Redis缓存过期时间(秒)")
    
    # PostgreSQL 配置
    database_url: str = Field(default="postgresql://user:pass@localhost/cee", description="数据库连接URL")
    
    # MinIO 配置
    minio_endpoint: str = Field(default="localhost:9000", description="MinIO服务端点")
    minio_access_key: str = Field(default="minioadmin", description="MinIO访问密钥")
    minio_secret_key: str = Field(default="minioadmin", description="MinIO秘密密钥")
    minio_bucket: str = Field(default="cee-data", description="MinIO存储桶")
    
    # 调度器配置
    scheduler_enabled: bool = Field(default=True, description="是否启用调度器")
    exam_board_interval: int = Field(default=86400, ge=3600, description="考试院爬虫间隔(秒)")
    university_interval: int = Field(default=604800, ge=3600, description="院校爬虫间隔(秒)")
    third_party_interval: int = Field(default=21600, ge=3600, description="第三方API间隔(秒)")
    
    class Config:
        env_file = ".env"
        env_prefix = "CEE_"
        
    def get_storage_config(self) -> dict:
        """获取存储配置字典"""
        return {
            'redis_url': self.redis_url,
            'database_url': self.database_url,
            'minio_endpoint': self.minio_endpoint,
            'minio_access_key': self.minio_access_key,
            'minio_secret_key': self.minio_secret_key,
            'minio_bucket': self.minio_bucket,
        }
    
    def get_spider_config(self) -> dict:
        """获取爬虫配置字典"""
        return {
            'timeout': self.request_timeout,
            'delay_min': self.request_delay_min,
            'delay_max': self.request_delay_max,
            'max_retries': self.max_retries,
            'mock_mode': self.mock_mode,
        }

# 全局配置实例
config = DataCollectorConfig()
