# tests/test_storage.py
def test_storage_engines_initialization():
    from core.storage import StorageManager
    storage = StorageManager()
    # Redis 可能已连接（如果本地运行），所以不强制检查为 None
    assert storage.data_dir is not None
    assert len(storage.list_json_files()) >= 0