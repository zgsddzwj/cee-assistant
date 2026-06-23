FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY cee-data-collector/ ./cee-data-collector/
COPY cee-recommendation/ ./cee-recommendation/
COPY cee-agent/ ./cee-agent/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r cee-data-collector/requirements.txt || true
RUN pip install --no-cache-dir fastapi uvicorn pydantic requests beautifulsoup4

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "cee-data-collector.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
