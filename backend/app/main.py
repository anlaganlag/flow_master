from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import api_router
from app.api.events import create_start_app_handler, create_stop_app_handler

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FlowMaster API - 高效任务管理系统的后端API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置事件处理器
app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "FlowMaster API is running"}

# 根路径重定向到文档
@app.get("/")
async def root():
    return {"message": "Welcome to FlowMaster API. Visit /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
