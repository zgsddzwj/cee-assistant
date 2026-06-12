# tests/test_scheduler.py
def test_scheduler_initializes_with_default_jobs():
    from core.scheduler import DataScheduler
    scheduler = DataScheduler()
    assert len(scheduler.jobs) == 3  # exam_board, university, third_party
    assert 'exam_board_spider' in scheduler.jobs
    assert 'university_spider' in scheduler.jobs
    assert 'third_party_api' in scheduler.jobs
