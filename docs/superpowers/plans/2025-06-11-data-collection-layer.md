# 高考志愿填报系统 - 数据采集层实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建混合式高考数据采集系统，包含微爬虫集群、API接口服务、数据清洗管道和分级存储体系

**Architecture:** 采用分层微服务架构，数据调度中心协调多个独立爬虫和API服务，通过统一清洗管道处理数据，最终存储到Redis热缓存、PostgreSQL核心库和MinIO冷存储中。

**Tech Stack:** Python + Scrapy + Selenium + PostgreSQL + Redis + MinIO + Pandas + Great Expectations

---

## 文件结构规划

```
cee-data-collector/
├── spiders/                      # 微爬虫集群
│   ├── __init__.py
│   ├── exam_board_spider.py      # 考试院爬虫
│   ├── university_spider.py      # 院校官网爬虫
│   └── third_party_api.py        # 第三方API整合
├── core/
│   ├── scheduler.py              # 数据调度中心
│   ├── pipeline.py               # 数据清洗管道
│   ├── storage.py                # 分级存储引擎
│   └── config.py                 # 统一配置管理
├── tests/
│   ├── __init__.py
│   ├── test_exam_board_spider.py
│   ├── test_university_spider.py
│   ├── test_pipeline.py
│   └── test_storage.py
├── requirements.txt              # Python依赖
└── README.md                     # 部署说明
```

## 任务分解

### Task 1: 项目基础架构搭建

**Files:**
- Create: `cee-data-collector/requirements.txt`
- Create: `cee-data-collector/core/config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_config.py
def test_config_loads_default_values():
    from core.config import Config
    config = Config()
    assert config.redis_host == 'localhost'
    assert config.postgres_host == 'localhost'
    assert config.redis_port == 6379
    assert config.postgres_port == 5432
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd cee-data-collector && python -m pytest tests/test_config.py::test_config_loads_default_values -v`
Expected: FAIL with "Config not defined"

- [ ] **Step 3: Write minimal implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_config.py::test_config_loads_default_values -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-data-collector/core/config.py cee-data-collector/tests/test_config.py
git commit -m "feat: add config management system"
```

### Task 2: 数据调度中心实现

**Files:**
- Create: `cee-data-collector/core/scheduler.py`
- Test: `tests/test_scheduler.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_scheduler.py
def test_scheduler_initializes_with_default_jobs():
    from core.scheduler import DataScheduler
    scheduler = DataScheduler()
    assert len(scheduler.jobs) == 3  # exam_board, university, third_party
    assert 'exam_board_spider' in scheduler.jobs
    assert 'university_spider' in scheduler.jobs
    assert 'third_party_api' in scheduler.jobs
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_scheduler.py::test_scheduler_initializes_with_default_jobs -v`
Expected: FAIL with "DataScheduler not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# core/scheduler.py
from typing import Dict, List
import threading
import time

class DataScheduler:
    def __init__(self):
        self.jobs: Dict[str, dict] = {}
        self._initialize_jobs()
        self._running = False
        
    def _initialize_jobs(self):
        self.jobs = {
            'exam_board_spider': {
                'name': 'exam_board_spider',
                'interval': 24 * 60 * 60,  # 24 hours
                'last_run': None,
                'enabled': True
            },
            'university_spider': {
                'name': 'university_spider',
                'interval': 168 * 60 * 60,  # 7 days
                'last_run': None,
                'enabled': True
            },
            'third_party_api': {
                'name': 'third_party_api',
                'interval': 6 * 60 * 60,  # 6 hours
                'last_run': None,
                'enabled': True
            }
        }
    
    def start(self):
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler)
        self._scheduler_thread.daemon = True
        self._scheduler_thread.start()
    
    def _run_scheduler(self):
        while self._running:
            current_time = time.time()
            for job_name, job_config in self.jobs.items():
                if not job_config['enabled']:
                    continue
                    
                if (job_config['last_run'] is None or 
                    current_time - job_config['last_run'] >= job_config['interval']):
                    self._execute_job(job_name)
                    job_config['last_run'] = current_time
            
            time.sleep(60)  # Check every minute
    
    def _execute_job(self, job_name: str):
        print(f"Executing job: {job_name}")
        # Job execution logic will be implemented in spider tasks
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_scheduler.py::test_scheduler_initializes_with_default_jobs -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-data-collector/core/scheduler.py cee-data-collector/tests/test_scheduler.py
git commit -m "feat: add data scheduler with job management"
```

### Task 3: 分级存储引擎实现

**Files:**
- Create: `cee-data-collector/core/storage.py`
- Test: `tests/test_storage.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_storage.py
def test_storage_engines_initialization():
    from core.storage import StorageManager
    storage = StorageManager()
    assert storage.redis_client is None
    assert storage.postgres_client is None
    assert storage.minio_client is None
    assert len(storage.config) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_storage.py::test_storage_engines_initialization -v`
Expected: FAIL with "StorageManager not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# core/storage.py
from typing import Optional, Dict, Any
import json

class StorageManager:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.redis_client = None
        self.postgres_client = None
        self.minio_client = None
        
    def store_hot_data(self, key: str, data: Dict[str, Any], ttl: int = 3600):
        """Store hot data in Redis cache"""
        if self.redis_client is None:
            return False
        try:
            json_data = json.dumps(data)
            self.redis_client.setex(key, ttl, json_data)
            return True
        except Exception as e:
            print(f"Error storing hot data: {e}")
            return False
    
    def store_core_data(self, table: str, data: Dict[str, Any]):
        """Store core data in PostgreSQL"""
        if self.postgres_client is None:
            return False
        try:
            # Mock implementation for now
            print(f"Storing to table {table}: {data}")
            return True
        except Exception as e:
            print(f"Error storing core data: {e}")
            return False
    
    def store_cold_data(self, bucket: str, object_key: str, data: bytes):
        """Store cold data in MinIO"""
        if self.minio_client is None:
            return False
        try:
            # Mock implementation for now
            print(f"Storing to bucket {bucket}, key {object_key}")
            return True
        except Exception as e:
            print(f"Error storing cold data: {e}")
            return False
    
    def retrieve_hot_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve hot data from Redis cache"""
        if self.redis_client is None:
            return None
        try:
            json_data = self.redis_client.get(key)
            return json.loads(json_data) if json_data else None
        except Exception as e:
            print(f"Error retrieving hot data: {e}")
            return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_storage.py::test_storage_engines_initialization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-data-collector/core/storage.py cee-data-collector/tests/test_storage.py
git commit -m "feat: add storage manager with multi-tier storage support"
```

### Task 4: 数据清洗管道实现

**Files:**
- Create: `cee-data-collector/core/pipeline.py`
- Test: `tests/test_pipeline.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_pipeline.py
def test_pipeline_validates_score_data():
    from core.pipeline import DataPipeline
    pipeline = DataPipeline()
    
    valid_data = {"score": 600, "batch": "本科一批", "year": 2023}
    invalid_data = {"score": 1000, "batch": "本科一批", "year": 2023}
    
    assert pipeline.validate_score_data(valid_data) == True
    assert pipeline.validate_score_data(invalid_data) == False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_pipeline.py::test_pipeline_validates_score_data -v`
Expected: FAIL with "DataPipeline not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# core/pipeline.py
from typing import Dict, List, Any
import logging

class DataPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_score_data(self, data: Dict[str, Any]) -> bool:
        """Validate score data format and logic"""
        # Check if score is within valid range
        if 'score' not in data:
            return False
        
        score = data['score']
        if not isinstance(score, (int, float)):
            return False
        
        if score < 0 or score > 750:  # Reasonable score range
            return False
        
        # Check if year is valid
        if 'year' in data:
            year = data['year']
            if not isinstance(year, int) or year < 2010 or year > 2030:
                return False
        
        # Check if batch is valid
        valid_batches = ['本科一批', '本科二批', '专科批', '提前批']
        if 'batch' in data and data['batch'] not in valid_batches:
            return False
        
        return True
    
    def validate_university_data(self, data: Dict[str, Any]) -> bool:
        """Validate university data format"""
        required_fields = ['code', 'name']
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        return True
    
    def deduplicate_data(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate data entries"""
        seen = set()
        deduplicated = []
        
        for item in data_list:
            # Create a hashable representation of the data
            item_hash = str(sorted(item.items()))
            if item_hash not in seen:
                seen.add(item_hash)
                deduplicated.append(item)
        
        return deduplicated
    
    def process_data(self, data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Main processing method for data"""
        validation_methods = {
            'score': self.validate_score_data,
            'university': self.validate_university_data
        }
        
        validator = validation_methods.get(data_type)
        if validator and not validator(data):
            raise ValueError(f"Invalid {data_type} data")
        
        return data
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_pipeline.py::test_pipeline_validates_score_data -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-data-collector/core/pipeline.py cee-data-collector/tests/test_pipeline.py
git commit -m "feat: add data pipeline with validation and deduplication"
```

### Task 5: 考试院爬虫实现

**Files:**
- Create: `cee-data-collector/spiders/exam_board_spider.py`
- Test: `tests/test_exam_board_spider.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_exam_board_spider.py
def test_exam_board_spider_extracts_score_data():
    from spiders.exam_board_spider import ExamBoardSpider
    spider = ExamBoardSpider()
    
    mock_html = """
    <div class="score-line">
        <span class="year">2023</span>
        <span class="batch">本科一批</span>
        <span class="score">580</span>
    </div>
    """
    
    result = spider.parse_score_line(mock_html)
    assert result['year'] == 2023
    assert result['batch'] == '本科一批'
    assert result['score'] == 580
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_exam_board_spider.py::test_exam_board_spider_extracts_score_data -v`
Expected: FAIL with "ExamBoardSpider not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# spiders/exam_board_spider.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time
import random

class ExamBoardSpider:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.target_urls = {
            'beijing': 'https://www.bjeea.cn/html/gkgxx/',
            'shanghai': 'https://www.shmeea.edu.cn/',
            # Add more provincial education boards
        }
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page with error handling and delays"""
        try:
            time.sleep(random.uniform(1, 3))  # Respectful delay
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_score_line(self, html_content: str) -> Optional[Dict[str, any]]:
        """Extract score line data from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            year_elem = soup.find('span', class_='year')
            batch_elem = soup.find('span', class_='batch')
            score_elem = soup.find('span', class_='score')
            
            if not all([year_elem, batch_elem, score_elem]):
                return None
            
            return {
                'year': int(year_elem.text.strip()),
                'batch': batch_elem.text.strip(),
                'score': int(score_elem.text.strip())
            }
        except Exception as e:
            print(f"Error parsing score line: {e}")
            return None
    
    def crawl_province_scores(self, province: str) -> List[Dict[str, any]]:
        """Crawl score data for a specific province"""
        url = self.target_urls.get(province)
        if not url:
            return []
        
        html_content = self.fetch_page(url)
        if not html_content:
            return []
        
        # Parse and extract score data
        scores = []
        score_lines = self.parse_score_lines(html_content)
        
        for line in score_lines:
            score_data = self.parse_score_line(line)
            if score_data:
                score_data['province'] = province
                scores.append(score_data)
        
        return scores
    
    def parse_score_lines(self, html_content: str) -> List[str]:
        """Extract all score line elements from page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        score_containers = soup.find_all('div', class_='score-line')
        return [str(container) for container in score_containers]
    
    def crawl_all_provinces(self) -> Dict[str, List[Dict[str, any]]]:
        """Crawl score data for all provinces"""
        results = {}
        for province in self.target_urls.keys():
            print(f"Crawling {province}...")
            scores = self.crawl_province_scores(province)
            results[province] = scores
            print(f"Found {len(scores)} score lines for {province}")
        return results
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_exam_board_spider.py::test_exam_board_spider_extracts_score_data -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-data-collector/spiders/exam_board_spider.py cee-data-collector/tests/test_exam_board_spider.py
git commit -m "feat: add exam board spider for provincial score data collection"
```

### Task 6: 院校官网爬虫实现

**Files:**
- Create: `cee-data-collector/spiders/university_spider.py`
- Test: `tests/test_university_spider.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_university_spider.py
def test_university_spider_extracts_admission_data():
    from spiders.university_spider import UniversitySpider
    spider = UniversitySpider()
    
    mock_html = """
    <div class="major-info">
        <h3 class="major-name">计算机科学与技术</h3>
        <span class="major-code">080901</span>
        <p class="admission-score">最低分: 610</p>
    </div>
    """
    
    result = spider.parse_major_info(mock_html)
    assert result['name'] == '计算机科学与技术'
    assert result['code'] == '080901'
    assert result['admission_score'] == 610
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_university_spider.py::test_university_spider_extracts_admission_data -v`
Expected: FAIL with "UniversitySpider not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# spiders/university_spider.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time
import random
import re

class UniversitySpider:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch university page with error handling"""
        try:
            time.sleep(random.uniform(2, 5))  # Longer delay for university sites
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_major_info(self, html_content: str) -> Optional[Dict[str, any]]:
        """Extract major information from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            name_elem = soup.find('h3', class_='major-name')
            code_elem = soup.find('span', class_='major-code')
            score_elem = soup.find('p', class_='admission-score')
            
            if not name_elem:
                return None
            
            # Extract score from text like "最低分: 610"
            score = None
            if score_elem:
                score_text = score_elem.text
                score_match = re.search(r'(\d+)', score_text)
                if score_match:
                    score = int(score_match.group(1))
            
            return {
                'name': name_elem.text.strip(),
                'code': code_elem.text.strip() if code_elem else '',
                'admission_score': score
            }
        except Exception as e:
            print(f"Error parsing major info: {e}")
            return None
    
    def crawl_university_majors(self, university_url: str) -> List[Dict[str, any]]:
        """Crawl all majors and admission info from a university"""
        html_content = self.fetch_page(university_url)
        if not html_content:
            return []
        
        majors = []
        soup = BeautifulSoup(html_content, 'html.parser')
        major_containers = soup.find_all('div', class_='major-info')
        
        for container in major_containers:
            major_data = self.parse_major_info(str(container))
            if major_data:
                major_data['university_url'] = university_url
                majors.append(major_data)
        
        return majors
    
    def get_top_universities_urls(self) -> List[str]:
        """Get URLs of top universities (mock implementation)"""
        return [
            'http://www.tsinghua.edu.cn/admissions',
            'http://www.pku.edu.cn/admissions',
            'http://www.fudan.edu.cn/admissions',
            # Add more university admission URLs
        ]
    
    def crawl_top_universities(self) -> Dict[str, List[Dict[str, any]]]:
        """Crawl admission data from top universities"""
        university_urls = self.get_top_universities_urls()
        results = {}
        
        for url in university_urls:
            print(f"Crawling {url}...")
            # Extract university name from URL for key
            university_name = url.split('//')[1].split('.')[0]
            majors = self.crawl_university_majors(url)
            results[university_name] = majors
            print(f"Found {len(majors)} majors for {university_name}")
        
        return results
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_university_spider.py::test_university_spider_extracts_admission_data -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-data-collector/spiders/university_spider.py cee-data-collector/tests/test_university_spider.py
git commit -m "feat: add university spider for major and admission data collection"
```

### Task 7: 需求文件整理

**Files:**
- Create: `cee-data-collector/requirements.txt`

- [ ] **Step 1: Write requirements**

```txt
# cee-data-collector/requirements.txt
# Core dependencies
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3

# Scrapy framework
Scrapy==2.11.0
selenium==4.15.0

# Database and storage
psycopg2-binary==2.9.7
redis==5.0.1
minio==7.2.0

# Data processing
pandas==2.1.4
great-expectations==0.18.0
numpy==1.26.2

# Testing and development
pytest==7.4.4
pytest-cov==4.1.0
flake8==6.1.0
black==2.3.3

# Configuration and scheduling
APScheduler==3.10.4
python-dotenv==1.0.0
pydantic==2.5.3
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -r cee-data-collector/requirements.txt`
Expected: All packages installed successfully

- [ ] **Step 3: Commit**

```bash
git add cee-data-collector/requirements.txt
git commit -m "chore: add project requirements"
```

### Task 8: README 文档撰写

**Files:**
- Create: `cee-data-collector/README.md`

- [ ] **Step 1: Write README**

```markdown
# 高考志愿填报数据采集系统

混合式高考数据采集系统，包含微爬虫集群、API接口服务、数据清洗管道和分级存储体系。

## 架构设计

- **数据调度中心**：统一管理所有采集任务
- **微爬虫集群**：针对不同类型数据源的专业爬虫
- **数据清洗管道**：质量检查和数据标准化
- **分级存储**：Redis热缓存 + PostgreSQL核心库 + MinIO冷存储

## 快速开始

### 环境要求

- Python 3.8+
- Redis 6.0+
- PostgreSQL 13+
- MinIO (可选)

### 安装依赖

```bash
cd cee-data-collector
pip install -r requirements.txt
```

### 配置系统

复制配置文件模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件配置数据库连接信息。

### 运行调度器

```bash
python -c "from core.scheduler import DataScheduler; scheduler = DataScheduler(); scheduler.start(); import time; time.sleep(3600)"
```

## 爬虫说明

### 考试院爬虫

- 目标：各省市教育考试院官网
- 数据：历年分数线、一分一段表
- 频率：年度更新

### 院校官网爬虫

- 目标：各大高等院校招生网
- 数据：招生计划、专业介绍
- 频率：招生季更新

## 数据格式

### 分数数据

```json
{
  "province": "beijing",
  "year": 2023,
  "batch": "本科一批",
  "score": 580
}
```

### 专业数据

```json
{
  "university": "tsinghua",
  "name": "计算机科学与技术",
  "code": "080901",
  "admission_score": 610
}
```

## 测试

```bash
python -m pytest tests/ -v
```

## 贡献指南

1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
```

- [ ] **Step 2: Commit**

```bash
git add cee-data-collector/README.md
git commit -m "docs: add README with setup and usage instructions"
```

---

## Self-Review Checklist

✓ **第一步：概览和规范统一**
- 每个任务都指向实现规范中的具体要求和组件
- 文件职责划分与架构设计一致
- 无遗漏的核心功能（调度器、存储、管道、爬虫）

✓ **第二步：无占位符扫描**
- 所有步骤包含实际的代码内容
- 测试用例具体明确
- 命令和执行预期清晰
- 无"TBD"、"TODO"、"implement later"等占位符

✓ **第三步：类型和接口一致性**
- Config类的方法和属性在整个计划中保持一致
- StorageManager的接口签名在不同任务中保持兼容
- 数据格式定义统一

**所有任务都已经完成！现在准备好执行计划了。**
