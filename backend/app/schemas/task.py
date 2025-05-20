from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class TaskBase(BaseModel):
    """任务基本信息"""
    title: Optional[str] = None
    description: Optional[str] = None
    list_type: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

class TaskCreate(TaskBase):
    """创建任务请求模型"""
    title: str
    list_type: str

class TaskUpdate(TaskBase):
    """更新任务请求模型"""
    is_completed: Optional[bool] = None

class TaskInDBBase(TaskBase):
    """数据库中的任务模型基类"""
    id: str
    user_id: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Task(TaskInDBBase):
    """API响应中的任务模型"""
    pass
