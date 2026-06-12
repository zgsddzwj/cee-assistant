# gateway/main.py
from fastapi import FastAPI
from gateway.router import recommendation_router

app = FastAPI(
    title="高考志愿填报推荐系统",
    description="基于AI的个性化高考志愿推荐服务",
    version="0.1.0"
)

app.include_router(recommendation_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recommendation"}