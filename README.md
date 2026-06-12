# CEE Assistant

高考志愿填报AI助手 - 基于深度学习和大数据的智能志愿填报系统。

## 项目架构

本项目采用微服务架构，包含四个核心模块：

```
cee-assistant/
├── cee-data-collector/      # 数据采集层
├── cee-recommendation/        # AI推荐引擎
├── cee-agent/                 # 智能咨询Agent
└── cee-frontend/              # 前端交互层
```

## 模块说明

### 1. 数据采集层 (`cee-data-collector`)
- **功能**：采集各省市考试院分数线、一分一段表、院校招生计划
- **技术**：Scrapy、BeautifulSoup、Selenium、Redis/PostgreSQL/MinIO
- **数据**：支持31个省市、50+所院校、600+专业

### 2. AI推荐引擎 (`cee-recommendation`)
- **功能**：基于混合推荐算法生成个性化志愿推荐
- **技术**：FastAPI、DeepSeek API、协同过滤、规则引擎
- **算法**：Rule Engine + Collaborative Filter + DeepSeek Agent

### 3. 智能咨询Agent (`cee-agent`)
- **功能**：多轮对话式志愿填报咨询
- **技术**：意图识别、对话管理、记忆系统
- **能力**：分数查询、专业咨询、院校对比、政策解读

### 4. 前端交互层 (`cee-frontend`)
- **功能**：用户界面、志愿填报可视化、聊天咨询
- **技术**：React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 18+
- Redis 6.0+ (可选)
- PostgreSQL 13+ (可选)

### 安装依赖

```bash
# 数据采集层
cd cee-data-collector
uv venv
uv pip install -e ".[dev]"

# 推荐引擎
cd cee-recommendation
uv venv
uv pip install -e ".[dev]"

# 智能Agent
cd cee-agent
uv venv
uv pip install -e ".[dev]"

# 前端
cd cee-frontend
npm install
```

### 运行项目

```bash
# 生成模拟数据（用于开发测试）
cd cee-data-collector
uv run python data_generator.py --year 2024

# 启动推荐引擎
cd cee-recommendation
uv run uvicorn gateway.main:app --reload

# 启动前端开发服务器
cd cee-frontend
npm run dev
```

## 数据说明

本项目使用**模拟数据**进行开发和测试，数据包括：
- 31个省市历年分数线
- 一分一段表（分数段排名）
- 50所重点院校招生计划
- 600+专业录取分数

> ⚠️ **注意**：模拟数据仅供开发测试使用，实际使用时需要替换为真实数据。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS, Zustand, shadcn/ui |
| 后端 | Python, FastAPI, Pydantic, Uvicorn |
| 数据 | Scrapy, BeautifulSoup, Pandas, NumPy |
| AI | DeepSeek API, 协同过滤, 规则引擎 |
| 存储 | Redis, PostgreSQL, MinIO, JSON |

## 开发文档

- [数据采集层设计文档](docs/superpowers/specs/2025-06-11-cee-data-collection-design.md)
- [推荐引擎设计文档](docs/superpowers/specs/2025-06-11-ai-recommendation-engine-design.md)
- [Agent咨询层设计文档](docs/superpowers/specs/2025-06-11-agent-consultation-layer-design.md)
- [前端交互层设计文档](docs/superpowers/specs/2025-06-11-frontend-interaction-layer-design.md)

## 贡献指南

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

## 许可证

MIT License
