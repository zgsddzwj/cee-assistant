# tests/test_exam_board_spider.py
def test_exam_board_spider_extracts_score_data():
    from spiders.exam_board_spider import ExamBoardSpider
    spider = ExamBoardSpider()
    
    # 测试爬虫能正确生成模拟数据
    scores = spider.generate_mock_score_data('beijing', 2024)
    assert len(scores) > 0
    
    score = scores[0]
    assert 'province' in score
    assert 'year' in score
    assert 'batch' in score
    assert 'score' in score
    assert score['province'] == 'beijing'