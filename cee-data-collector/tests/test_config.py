# tests/test_config.py
def test_config_loads_default_values():
    from core.config import Config
    config = Config()
    assert config.redis_host == 'localhost'
    assert config.postgres_host == 'localhost'
    assert config.redis_port == 6379
    assert config.postgres_port == 5432
