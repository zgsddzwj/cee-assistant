# tests/test_university_spider.py
def test_university_spider_extracts_admission_data():
    from spiders.university_spider import UniversitySpider
    spider = UniversitySpider()
    
    # 测试爬虫能正确生成模拟数据
    data = spider.generate_mock_university_data('tsinghua', 2024)
    assert data['university_name'] == '清华大学'
    assert len(data['majors']) > 0
    
    major = data['majors'][0]
    assert 'name' in major
    assert 'code' in major
    assert 'admission_score' in major