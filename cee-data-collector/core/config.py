# core/config.py
class Config:
    def __init__(self):
        # Database configuration
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.postgres_host = 'localhost'
        self.postgres_port = 5432
        
        # Collection configuration
        self.user_agent = 'GaokaoDataCollector/1.0'
        self.request_delay = 1.0
        self.retry_attempts = 3
        self.concurrent_requests = 5
