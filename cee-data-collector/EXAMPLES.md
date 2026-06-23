# CEE Data Collector 使用示例

## 快速开始

### 1. 生成模拟数据

```bash
cd cee-data-collector
uv run python data_generator.py --year 2024
```

### 2. 使用 CLI 工具

```bash
# 查看系统状态
uv run python cli.py status

# 验证数据
uv run python cli.py validate data/all_scores_2024.json --type score

# 运行爬虫
uv run python cli.py run-spider --type all

# 系统监控
uv run python cli.py monitor
```

### 3. 使用搜索服务

```python
from services.search_service import UniversitySearchService, SearchCriteria

# 加载数据
import json
with open('data/all_universities_2024.json') as f:
    universities = json.load(f)

# 创建搜索服务
service = UniversitySearchService(universities)

# 搜索院校
criteria = SearchCriteria(
    keyword="清华",
    province="北京",
    min_score=650
)
results = service.search(criteria)
print(f"找到 {results['total']} 所院校")
```

### 4. 使用推荐服务

```python
from services.recommendation_service import RecommendationService

service = RecommendationService(universities)

# 获取推荐
recommendations = service.recommend(
    score=680,
    rank=5000,
    province="北京",
    subject_type="综合",
    interests=["计算机", "编程"]
)

for rec in recommendations[:5]:
    print(f"{rec.university['university_name']} - {rec.major['name']}")
    print(f"  匹配度: {rec.match_score:.1f}%, 概率: {rec.probability}")
    print(f"  类型: {rec.rec_type.value}, 原因: {', '.join(rec.reasons)}")
```

### 5. 使用分析服务

```python
from services.analytics_service import AnalyticsService

# 加载分数线数据
with open('data/all_scores_2024.json') as f:
    scores = json.load(f)

service = AnalyticsService(scores=scores, universities=universities)

# 分析趋势
trend = service.analyze_score_trend("beijing", "本科一批", [2022, 2023, 2024])
print(f"趋势: {trend['trend']}, 平均变化: {trend['avg_change']}")

# 院校难度排名
difficulty = service.analyze_university_difficulty()
for uni in difficulty[:10]:
    print(f"{uni['university_name']}: 平均分 {uni['avg_score']}")
```

### 6. 导出数据

```python
from utils.exporter import DataExporter

exporter = DataExporter()

# 导出为 CSV
exporter.export_scores(scores, format="csv")

# 导出为 Excel
exporter.export_universities(universities, format="excel")

# 批量导出
exporter.batch_export({
    "scores": scores,
    "universities": universities
}, format="csv")
```

### 7. 启动 API 服务

```bash
# 安装依赖
pip install fastapi uvicorn

# 启动服务
uvicorn cee-data-collector.api.main:app --reload

# 访问文档
open http://localhost:8000/docs
```

### 8. Docker 部署

```bash
# 构建镜像
docker build -t cee-data-collector .

# 运行容器
docker run -p 8000:8000 cee-data-collector
```

## API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 服务状态 |
| `/universities` | GET | 院校列表 |
| `/universities/{id}` | GET | 院校详情 |
| `/recommend` | POST | 志愿推荐 |
| `/analytics/trend` | GET | 分数线趋势 |
| `/analytics/difficulty` | GET | 难度排名 |
| `/health` | GET | 健康检查 |
