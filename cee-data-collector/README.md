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

本项目使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理。

```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境并安装依赖
cd cee-data-collector
uv venv
uv pip install -e ".[dev]"
```

### 开发工作流

```bash
# 添加新依赖
uv add <package-name>

# 添加开发依赖
uv add --dev <package-name>

# 同步依赖（根据 pyproject.toml）
uv pip install -e ".[dev]"

# 运行测试
uv run pytest

# 格式化代码
uv run black .
```

### 使用 uv 运行脚本

```bash
# 直接运行 Python 脚本（自动使用虚拟环境）
uv run python -c "from core.scheduler import DataScheduler; scheduler = DataScheduler()"
```

### 锁定依赖版本

```bash
# 生成 uv.lock 锁定文件
uv pip compile pyproject.toml -o uv.lock

# 根据锁定文件安装（可复现构建）
uv pip sync uv.lock
```

### 配置系统

复制配置文件模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件配置数据库连接信息。

### 运行调度器

```bash
uv run python -c "from core.scheduler import DataScheduler; scheduler = DataScheduler(); scheduler.start(); import time; time.sleep(3600)"
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
uv run pytest tests/ -v
```

## 贡献指南

1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
</content>
</invoke>

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