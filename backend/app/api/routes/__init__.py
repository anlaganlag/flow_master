from fastapi import APIRouter
from app.api.routes import auth, tasks, daily_cards

api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["任务"])
api_router.include_router(daily_cards.router, prefix="/daily-cards", tags=["每日卡片"])
