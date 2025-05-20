from fastapi import FastAPI
from app.core.db import connect_to_mongo, close_mongo_connection

def create_start_app_handler(app: FastAPI):
    """
    创建应用启动处理器
    """
    async def start_app() -> None:
        await connect_to_mongo()
    
    return start_app

def create_stop_app_handler(app: FastAPI):
    """
    创建应用停止处理器
    """
    async def stop_app() -> None:
        await close_mongo_connection()
    
    return stop_app
