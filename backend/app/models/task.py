from datetime import datetime
from typing import Optional, List
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.user import PyObjectId

class ListType(str, Enum):
    """任务列表类型枚举"""
    TODO = "todo"
    WATCH = "watch"
    LATER = "later"

class TaskBase(BaseModel):
    """任务基本信息"""
    title: str
    description: Optional[str] = None
    list_type: ListType
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True

class TaskCreate(TaskBase):
    """创建任务时的数据模型"""
    pass

class TaskUpdate(BaseModel):
    """更新任务时的数据模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    list_type: Optional[ListType] = None
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    is_completed: Optional[bool] = None

class TaskInDB(TaskBase):
    """数据库中的任务模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Task(TaskInDB):
    """API响应中的任务模型"""
    pass
