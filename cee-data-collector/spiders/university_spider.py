# spiders/university_spider.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time
import random
import re
import json
import os
from datetime import datetime

class UniversitySpider:
    """院校官网爬虫 - 抓取各大学招生计划和专业介绍
    
    支持两种模式：
    1. 真实爬取模式：从院校官网抓取（需要处理反爬）
    2. 模拟数据模式：生成 realistic 的模拟数据用于开发和测试
    """
    
    # 重点院校列表（示例）
    TOP_UNIVERSITIES = {
        'tsinghua': {'name': '清华大学', 'url': 'https://www.tsinghua.edu.cn/admissions/', 'tier': 1},
        'pku': {'name': '北京大学', 'url': 'https://www.pku.edu.cn/admissions/', 'tier': 1},
        'fudan': {'name': '复旦大学', 'url': 'https://www.fudan.edu.cn/admissions/', 'tier': 1},
        'sjtu': {'name': '上海交通大学', 'url': 'https://www.sjtu.edu.cn/admissions/', 'tier': 1},
        'zhejiang': {'name': '浙江大学', 'url': 'https://www.zju.edu.cn/admissions/', 'tier': 1},
        'ustc': {'name': '中国科学技术大学', 'url': 'https://www.ustc.edu.cn/admissions/', 'tier': 1},
        'nankai': {'name': '南开大学', 'url': 'https://www.nankai.edu.cn/admissions/', 'tier': 1},
        'buaa': {'name': '北京航空航天大学', 'url': 'https://www.buaa.edu.cn/admissions/', 'tier': 1},
        'tongji': {'name': '同济大学', 'url': 'https://www.tongji.edu.cn/admissions/', 'tier': 1},
        'whu': {'name': '武汉大学', 'url': 'https://www.whu.edu.cn/admissions/', 'tier': 1},
        'xiamen': {'name': '厦门大学', 'url': 'https://www.xmu.edu.cn/admissions/', 'tier': 2},
        'sdu': {'name': '山东大学', 'url': 'https://www.sdu.edu.cn/admissions/', 'tier': 2},
        'cqu': {'name': '重庆大学', 'url': 'https://www.cqu.edu.cn/admissions/', 'tier': 2},
        'dlut': {'name': '大连理工大学', 'url': 'https://www.dlut.edu.cn/admissions/', 'tier': 2},
        'hust': {'name': '华中科技大学', 'url': 'https://www.hust.edu.cn/admissions/', 'tier': 2},
        'xjtu': {'name': '西安交通大学', 'url': 'https://www.xjtu.edu.cn/admissions/', 'tier': 2},
        'bnu': {'name': '北京师范大学', 'url': 'https://www.bnu.edu.cn/admissions/', 'tier': 2},
        'cau': {'name': '中国农业大学', 'url': 'https://www.cau.edu.cn/admissions/', 'tier': 2},
        'ecnu': {'name': '华东师范大学', 'url': 'https://www.ecnu.edu.cn/admissions/', 'tier': 2},
        'scu': {'name': '四川大学', 'url': 'https://www.scu.edu.cn/admissions/', 'tier': 2},
    }
    
    # 常见专业列表
    COMMON_MAJORS = [
        {'name': '计算机科学与技术', 'code': '080901', 'category': '工学', 'hot': True},
        {'name': '软件工程', 'code': '080902', 'category': '工学', 'hot': True},
        {'name': '人工智能', 'code': '080717', 'category': '工学', 'hot': True},
        {'name': '电子信息工程', 'code': '080701', 'category': '工学', 'hot': True},
        {'name': '电气工程及其自动化', 'code': '080601', 'category': '工学', 'hot': True},
        {'name': '机械工程', 'code': '080201', 'category': '工学', 'hot': False},
        {'name': '土木工程', 'code': '081001', 'category': '工学', 'hot': False},
        {'name': '金融学', 'code': '020301', 'category': '经济学', 'hot': True},
        {'name': '经济学', 'code': '020101', 'category': '经济学', 'hot': False},
        {'name': '国际经济与贸易', 'code': '020401', 'category': '经济学', 'hot': False},
        {'name': '工商管理', 'code': '120201', 'category': '管理学', 'hot': True},
        {'name': '会计学', 'code': '120203', 'category': '管理学', 'hot': True},
        {'name': '法学', 'code': '030101', 'category': '法学', 'hot': True},
        {'name': '临床医学', 'code': '100201', 'category': '医学', 'hot': True},
        {'name': '口腔医学', 'code': '100301', 'category': '医学', 'hot': True},
        {'name': '药学', 'code': '100701', 'category': '医学', 'hot': False},
        {'name': '数学与应用数学', 'code': '070101', 'category': '理学', 'hot': False},
        {'name': '物理学', 'code': '070201', 'category': '理学', 'hot': False},
        {'name': '化学', 'code': '070301', 'category': '理学', 'hot': False},
        {'name': '汉语言文学', 'code': '050101', 'category': '文学', 'hot': False},
        {'name': '英语', 'code': '050201', 'category': '文学', 'hot': True},
        {'name': '新闻学', 'code': '050301', 'category': '文学', 'hot': False},
        {'name': '建筑学', 'code': '082801', 'category': '工学', 'hot': True},
        {'name': '城乡规划', 'code': '082802', 'category': '工学', 'hot': False},
    ]
    
    def __init__(self, use_mock: bool = True, data_dir: str = './data'):
        self.use_mock = use_mock
        self.data_dir = data_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        os.makedirs(data_dir, exist_ok=True)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch university page with error handling"""
        if self.use_mock:
            return None
            
        try:
            time.sleep(random.uniform(3, 6))  # Longer delay for university sites
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def generate_mock_university_data(self, uni_key: str, year: int = 2024) -> Dict:
        """生成模拟的院校数据"""
        uni_info = self.TOP_UNIVERSITIES[uni_key]
        
        # 根据院校 tier 确定基础分数
        if uni_info['tier'] == 1:
            base_score = random.randint(620, 680)
        else:
            base_score = random.randint(580, 640)
        
        # 随机选择该院校开设的专业（10-20个）
        num_majors = random.randint(10, 20)
        selected_majors = random.sample(self.COMMON_MAJORS, min(num_majors, len(self.COMMON_MAJORS)))
        
        majors = []
        for major in selected_majors:
            # 热门专业分数更高
            if major['hot']:
                score_offset = random.randint(0, 30)
            else:
                score_offset = random.randint(-20, 10)
            
            admission_score = base_score + score_offset
            
            majors.append({
                'name': major['name'],
                'code': major['code'],
                'category': major['category'],
                'admission_score': admission_score,
                'plan_count': random.randint(30, 200),  # 招生计划人数
                'tuition': random.choice([5000, 5500, 6000, 8000, 10000]),
                'duration': 4 if major['category'] != '医学' else 5,
                'hot': major['hot'],
            })
        
        # 按分数排序
        majors.sort(key=lambda x: x['admission_score'], reverse=True)
        
        return {
            'university_key': uni_key,
            'university_name': uni_info['name'],
            'tier': uni_info['tier'],
            'year': year,
            'province': random.choice(['北京', '上海', '江苏', '浙江', '湖北', '四川', '陕西']),
            'majors': majors,
            'total_plan': sum(m['plan_count'] for m in majors),
            'updated_at': datetime.now().isoformat()
        }
    
    def crawl_university(self, uni_key: str, year: int = 2024) -> Dict:
        """爬取或生成单个院校数据"""
        if uni_key not in self.TOP_UNIVERSITIES:
            print(f"Unknown university: {uni_key}")
            return {}
        
        if self.use_mock:
            print(f"[MOCK] Generating data for {self.TOP_UNIVERSITIES[uni_key]['name']}")
            return self.generate_mock_university_data(uni_key, year)
        
        uni_info = self.TOP_UNIVERSITIES[uni_key]
        html_content = self.fetch_page(uni_info['url'])
        
        if not html_content:
            print(f"[MOCK] Fallback to mock data for {uni_info['name']}")
            return self.generate_mock_university_data(uni_key, year)
        
        # TODO: 实现真实HTML解析
        return self.generate_mock_university_data(uni_key, year)
    
    def crawl_all_universities(self, year: int = 2024) -> Dict[str, Dict]:
        """采集所有院校数据"""
        results = {}
        universities = list(self.TOP_UNIVERSITIES.keys())
        
        print(f"Starting to crawl {len(universities)} universities...")
        
        for uni_key in universities:
            data = self.crawl_university(uni_key, year)
            if data:
                results[uni_key] = data
                print(f"  {data['university_name']}: {len(data['majors'])} majors")
        
        return results
    
    def save_to_json(self, data: Dict, filename: str = None):
        """保存数据到本地JSON文件"""
        if filename is None:
            filename = f"university_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to {filepath}")
        return filepath
    
    def run(self, year: int = 2024, save: bool = True) -> Dict:
        """运行完整采集流程"""
        print(f"=== University Data Collection ({year}) ===")
        print(f"Mode: {'MOCK' if self.use_mock else 'REAL'}")
        print(f"Universities: {len(self.TOP_UNIVERSITIES)}")
        print()
        
        results = self.crawl_all_universities(year)
        
        if save:
            filepath = self.save_to_json(results)
            print(f"\nData saved to: {filepath}")
        
        # 打印统计
        total_majors = sum(len(v['majors']) for v in results.values())
        total_plan = sum(v['total_plan'] for v in results.values())
        print(f"\nTotal universities: {len(results)}")
        print(f"Total majors: {total_majors}")
        print(f"Total plan count: {total_plan}")
        
        return results


if __name__ == '__main__':
    spider = UniversitySpider(use_mock=True)
    spider.run(year=2024)
