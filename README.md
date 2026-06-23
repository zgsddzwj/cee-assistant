# CEE Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/Node-18+-green.svg" alt="Node 18+">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/FastAPI-0.104+-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18+-61DAFB.svg" alt="React 18">
</p>

<p align="center">
  <b>高考志愿填报AI助手</b> - 基于深度学习和大数据的智能志愿填报系统
</p>

---

## 项目简介

CEE Assistant 是一个面向高考考生的智能志愿填报辅助系统，采用微服务架构，整合数据采集、AI推荐、智能咨询和前端交互四大模块，为考生提供个性化、数据驱动的志愿填报建议。

## 核心功能

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| 数据采集 | 31省市分数线、一分一段表、院校招生计划 | ✅ 完成 |
| 智能推荐 | 基于分数/兴趣/地域的多维推荐算法 | ✅ 完成 |
| 院校搜索 | 多维度筛选、分页排序、关键词搜索 | ✅ 完成 |
| 数据分析 | 分数线趋势、院校难度排名、专业热度 | ✅ 完成 |
| 智能咨询 | 多轮对话式志愿填报咨询 | ✅ 完成 |
| 数据导出 | CSV/Excel/JSON 格式导出 | ✅ 完成 |
| 数据比对 | 历年数据差异分析 | ✅ 完成 |
| 可视化 | HTML 趋势报表、分布统计 | ✅ 完成 |
| 用户管理 | 考生档案、查询历史 | ✅ 完成 |
| 备份恢复 | 自动压缩备份、版本管理 | ✅ 完成 |
| API 服务 | FastAPI RESTful 接口 + 自动文档 | ✅ 完成 |
| Docker | 容器化部署支持 | ✅ 完成 |

## 项目架构

```
cee-assistant/
├── cee-data-collector/      # 数据采集层
│   ├── spiders/              # 爬虫模块（考试院、院校）
│   ├── core/                 # 核心组件（调度器、存储、配置）
│   ├── services/             # 服务层（搜索、推荐、分析）
│   ├── models/               # 数据模型（Pydantic Schema）
│   ├── utils/                # 工具类（导出、缓存、监控）
│   ├── api/                  # FastAPI 接口
│   └── cli.py               # 命令行工具
├── cee-recommendation/       # AI推荐引擎
│   ├── gateway/             # API 网关
│   ├── services/            # 推荐算法（规则+协同过滤+LLM）
│   └── models/              # 数据模型
├── cee-agent/               # 智能咨询Agent
│   ├── agent/               # Agent 核心（意图识别、对话管理）
│   └── models/              # 数据模型
└── cee-frontend/            # 前端交互层
    ├── src/
    │   ├── pages/           # 页面（首页、聊天、推荐）
    │   ├── components/     # 组件（布局、聊天、推荐卡片）
    │   ├── stores/         # 状态管理（Zustand）
    │   └── api/            # API 客户端
    └── public/
```

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
# 1. 生成模拟数据
cd cee-data-collector
uv run python data_generator.py --year 2024

# 2. 启动数据采集 API
cd cee-data-collector
uv run uvicorn api.main:app --reload --port 8001

# 3. 启动推荐引擎
cd cee-recommendation
uv run uvicorn gateway.main:app --reload --port 8002

# 4. 启动前端开发服务器
cd cee-frontend
npm run dev
```

访问 http://localhost:5173 查看前端界面

## CLI 工具使用

```bash
cd cee-data-collector

# 生成模拟数据
uv run python cli.py generate-data --year 2024

# 运行爬虫
uv run python cli.py run-spider --type all

# 查看系统状态
uv run python cli.py status

# 验证数据质量
uv run python cli.py validate data/all_scores_2024.json --type score

# 系统监控
uv run python cli.py monitor --export metrics.json
```

## API 接口

启动服务后访问 http://localhost:8001/docs 查看自动生成的 Swagger 文档。

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 服务状态 |
| `/universities` | GET | 院校列表（支持筛选、分页） |
| `/universities/{id}` | GET | 院校详情 |
| `/recommend` | POST | 志愿推荐 |
| `/analytics/trend` | GET | 分数线趋势分析 |
| `/analytics/difficulty` | GET | 院校难度排名 |
| `/health` | GET | 健康检查 |

### 推荐接口示例

```bash
curl -X POST "http://localhost:8001/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "score": 600,
    "rank": 15000,
    "province": "beijing",
    "subject_type": "综合",
    "interests": ["编程", "数学"],
    "career_plan": "软件工程师"
  }'
```

## Docker 部署

```bash
# 构建镜像
docker build -t cee-assistant .

# 运行容器
docker run -p 8000:8000 cee-assistant

# 访问 API
curl http://localhost:8000/health
```

## 数据说明

本项目使用**模拟数据**进行开发和测试：

| 数据类型 | 数量 | 说明 |
|---------|------|------|
| 省市 | 31个 | 全国各省市 |
| 分数线记录 | 465条 | 历年各批次分数线 |
| 一分一段表 | 51,150条 | 分数段排名数据 |
| 院校 | 50所 | 985/211/重点院校 |
| 专业 | 611个 | 涵盖工学、理学、经济学等 |

> ⚠️ **注意**：模拟数据仅供开发测试使用，实际使用时需要替换为真实数据。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS, Zustand, shadcn/ui, Axios |
| 后端 | Python, FastAPI, Pydantic, Uvicorn, httpx |
| 数据 | Scrapy, BeautifulSoup, Pandas, NumPy, aiohttp |
| AI | DeepSeek API, 协同过滤, 规则引擎 |
| 存储 | Redis, PostgreSQL, MinIO, JSON 文件 |
| 监控 | 结构化日志, 性能指标, 健康检查 |
| 部署 | Docker, uv 包管理 |

## 开发文档

- [数据采集层设计文档](docs/superpowers/specs/2025-06-11-cee-data-collection-design.md)
- [推荐引擎设计文档](docs/superpowers/specs/2025-06-11-ai-recommendation-engine-design.md)
- [Agent咨询层设计文档](docs/superpowers/specs/2025-06-11-agent-consultation-layer-design.md)
- [前端交互层设计文档](docs/superpowers/specs/2025-06-11-frontend-interaction-layer-design.md)
- [使用示例](cee-data-collector/EXAMPLES.md)

## 项目统计

- **代码文件**: 100+
- **测试覆盖**: 6个核心模块
- **API 端点**: 7个
- **CLI 命令**: 5个
- **数据量**: 50+院校, 600+专业, 31省市

## 贡献指南

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'feat: Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

## 许可证

MIT License

---

<p align="center">
  Made with ❤️ for CEE Candidates
</p>

---

## 更新日志

### v1.1.0 (2024-06)
- 新增数据比对和差异分析功能
- 新增数据可视化报表（HTML趋势图）
- 新增院校搜索和筛选服务
- 新增专业推荐算法（冲/稳/保）
- 新增分数线趋势分析
- 新增用户偏好配置管理
- 新增数据备份和恢复功能
- 新增 FastAPI RESTful API
- 新增 Docker 容器化支持
- 完善项目文档和示例

### v1.0.0 (2024-06)
- 初始版本发布
- 完成数据采集层（考试院爬虫、院校爬虫）
- 完成推荐引擎（规则引擎、协同过滤）
- 完成智能咨询 Agent（意图识别、对话管理）
- 完成前端交互层（React + TypeScript）
- 生成模拟数据（31省市、50院校、600+专业）

## 贡献者

感谢所有为项目做出贡献的开发者：

- [CEE Assistant Team](https://github.com/zgsddzwj)

## 相关链接

- [项目主页](https://github.com/zgsddzwj/cee-assistant)
- [问题反馈](https://github.com/zgsddzwj/cee-assistant/issues)
- [更新日志](https://github.com/zgsddzwj/cee-assistant/releases)