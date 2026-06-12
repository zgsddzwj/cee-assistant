# spiders/exam_board_spider.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time
import random
import json
import os
from datetime import datetime

class ExamBoardSpider:
    """考试院爬虫 - 抓取各省市历年分数线和一分一段表
    
    支持两种模式：
    1. 真实爬取模式：从各省市教育考试院官网抓取（需要处理反爬）
    2. 模拟数据模式：生成 realistic 的模拟数据用于开发和测试
    """
    
    # 全国31省市教育考试院官网（部分示例）
    PROVINCIAL_URLS = {
        'beijing': 'https://www.bjeea.cn/html/gkgxx/',
        'shanghai': 'https://www.shmeea.edu.cn/',
        'guangdong': 'https://eea.gd.gov.cn/',
        'jiangsu': 'https://www.jseea.cn/',
        'zhejiang': 'https://www.zjzs.net/',
        'shandong': 'http://www.sdzk.cn/',
        'henan': 'http://www.heao.gov.cn/',
        'sichuan': 'https://www.sceea.cn/',
        'hubei': 'http://www.hbea.edu.cn/',
        'hunan': 'https://jyt.hunan.gov.cn/',
        'hebei': 'http://www.hebeea.edu.cn/',
        'anhui': 'https://www.ahzsks.cn/',
        'jiangxi': 'http://www.jxeea.cn/',
        'fujian': 'https://www.eeafj.cn/',
        'shanxi': 'http://www.sxkszx.cn/',
        'shanxi2': 'http://www.sneea.cn/',  # 陕西
        'liaoning': 'https://www.lnzsks.com/',
        'jilin': 'http://www.jleea.edu.cn/',
        'heilongjiang': 'https://www.lzk.hl.cn/',
        'tianjin': 'http://www.zhaokao.net/',
        'chongqing': 'https://www.cqksy.cn/',
    }
    
    # 批次类型
    BATCHES = ['本科一批', '本科二批', '本科批', '专科批', '提前批']
    
    def __init__(self, use_mock: bool = True, data_dir: str = './data'):
        self.use_mock = use_mock
        self.data_dir = data_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page with error handling and delays"""
        if self.use_mock:
            return None
            
        try:
            time.sleep(random.uniform(2, 5))  # Respectful delay
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def generate_mock_score_data(self, province: str, year: int = 2024) -> List[Dict]:
        """生成模拟的分数线数据"""
        # 基于不同省份生成 realistic 的分数数据
        base_scores = {
            'beijing': 550, 'shanghai': 540, 'tianjin': 545,
            'guangdong': 530, 'jiangsu': 520, 'zhejiang': 535,
            'shandong': 520, 'henan': 515, 'sichuan': 525,
            'hubei': 510, 'hunan': 515, 'hebei': 500,
            'anhui': 505, 'jiangxi': 500, 'fujian': 510,
            'shanxi': 495, 'shanxi2': 505, 'liaoning': 500,
            'jilin': 490, 'heilongjiang': 485, 'chongqing': 515,
        }
        
        base = base_scores.get(province, 500)
        scores = []
        
        for batch in self.BATCHES:
            if '一批' in batch:
                score = base + random.randint(20, 40)
            elif '二批' in batch:
                score = base - random.randint(10, 30)
            elif '专科' in batch:
                score = base - random.randint(80, 120)
            elif '提前批' in batch:
                score = base + random.randint(30, 60)
            else:
                score = base
            
            scores.append({
                'province': province,
                'year': year,
                'batch': batch,
                'score': score,
                'subject_type': random.choice(['文科', '理科', '综合']),
                'updated_at': datetime.now().isoformat()
            })
        
        return scores
    
    def generate_mock_rank_data(self, province: str, year: int = 2024) -> List[Dict]:
        """生成模拟的一分一段表数据"""
        ranks = []
        # 生成从 700 分到 300 分的一分一段数据
        for score in range(700, 300, -1):
            # 分数越高，人数越少
            if score >= 650:
                count = random.randint(1, 20)
            elif score >= 600:
                count = random.randint(20, 100)
            elif score >= 550:
                count = random.randint(100, 500)
            elif score >= 500:
                count = random.randint(500, 2000)
            elif score >= 450:
                count = random.randint(2000, 5000)
            else:
                count = random.randint(5000, 15000)
            
            ranks.append({
                'province': province,
                'year': year,
                'score': score,
                'count': count,
                'cumulative_count': 0,  # 需要计算
                'subject_type': random.choice(['文科', '理科', '综合']),
                'updated_at': datetime.now().isoformat()
            })
        
        # 计算累计人数
        cumulative = 0
        for rank in ranks:
            cumulative += rank['count']
            rank['cumulative_count'] = cumulative
        
        return ranks
    
    def crawl_province_scores(self, province: str, year: int = 2024) -> List[Dict]:
        """爬取或生成指定省份的分数线数据"""
        if self.use_mock or province not in self.PROVINCIAL_URLS:
            print(f"[MOCK] Generating score data for {province} ({year})")
            return self.generate_mock_score_data(province, year)
        
        url = self.PROVINCIAL_URLS.get(province)
        html_content = self.fetch_page(url)
        
        if not html_content:
            print(f"[MOCK] Fallback to mock data for {province}")
            return self.generate_mock_score_data(province, year)
        
        # TODO: 实现真实HTML解析
        return self.generate_mock_score_data(province, year)
    
    def crawl_province_ranks(self, province: str, year: int = 2024) -> List[Dict]:
        """爬取或生成指定省份的一分一段表"""
        if self.use_mock:
            print(f"[MOCK] Generating rank data for {province} ({year})")
            return self.generate_mock_rank_data(province, year)
        
        # TODO: 实现真实爬取
        return self.generate_mock_rank_data(province, year)
    
    def crawl_all_provinces(self, year: int = 2024) -> Dict[str, Dict]:
        """采集所有省份的数据"""
        results = {
            'scores': {},
            'ranks': {}
        }
        
        provinces = list(self.PROVINCIAL_URLS.keys())
        print(f"Starting to crawl {len(provinces)} provinces...")
        
        for province in provinces:
            print(f"Processing {province}...")
            
            # 采集分数线
            scores = self.crawl_province_scores(province, year)
            results['scores'][province] = scores
            
            # 采集一分一段表
            ranks = self.crawl_province_ranks(province, year)
            results['ranks'][province] = ranks
            
            print(f"  Scores: {len(scores)} batches")
            print(f"  Ranks: {len(ranks)} score points")
        
        return results
    
    def save_to_json(self, data: Dict, filename: str = None):
        """保存数据到本地JSON文件"""
        if filename is None:
            filename = f"exam_board_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to {filepath}")
        return filepath
    
    def run(self, year: int = 2024, save: bool = True) -> Dict:
        """运行完整采集流程"""
        print(f"=== Exam Board Data Collection ({year}) ===")
        print(f"Mode: {'MOCK' if self.use_mock else 'REAL'}")
        print(f"Provinces: {len(self.PROVINCIAL_URLS)}")
        print()
        
        results = self.crawl_all_provinces(year)
        
        if save:
            filepath = self.save_to_json(results)
            print(f"\nData saved to: {filepath}")
        
        # 打印统计
        total_scores = sum(len(v) for v in results['scores'].values())
        total_ranks = sum(len(v) for v in results['ranks'].values())
        print(f"\nTotal score lines: {total_scores}")
        print(f"Total rank entries: {total_ranks}")
        
        return results


if __name__ == '__main__':
    spider = ExamBoardSpider(use_mock=True)
    spider.run(year=2024)
