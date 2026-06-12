# 高考志愿填报AI推荐引擎

基于混合推荐算法的高考志愿智能推荐系统。

## 架构

- **API Gateway** (FastAPI) - 统一入口
- **Rule Engine** - 基于分数位次的规则筛选
- **Collaborative Filter** - 相似考生群体智能
- **DeepSeek Agent** - AI个性化分析
- **Result Merger** - 多源结果融合排序

## 快速开始

```bash
# 安装依赖
uv venv
uv pip install -e ".[dev]"

# 启动服务
uv run uvicorn gateway.main:app --reload
```

## API 使用

```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "score": 600,
    "rank": 15000,
    "province": "北京",
    "subject_type": "综合",
    "interests": ["编程", "数学"],
    "career_plan": "软件工程师"
  }'
```

## 推荐流程

1. **Rule Engine** 初筛候选院校（±20分浮动）
2. **Collaborative Filter** 分析相似考生选择
3. **DeepSeek Agent** 生成个性化评分
4. **Result Merger** 综合排序，确保"冲稳保"分布

## 开发

```bash
# 运行测试
uv run pytest

# 格式化代码
uv run black .
```

## 环境变量

```bash
DEEPSEEK_API_KEY=your_api_key
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://user:pass@localhost/cee
```