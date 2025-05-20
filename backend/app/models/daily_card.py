from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.user import PyObjectId

class AccomplishmentSource(str, Enum):
    """成就来源枚举"""
    MANUAL = "manual"
    TASK = "task"

class CardTask(BaseModel):
    """卡片中的任务"""
    task_id: PyObjectId
    title: str
    is_completed: bool = False
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Accomplishment(BaseModel):
    """成就记录"""
    title: str
    source: AccomplishmentSource
    task_id: Optional[PyObjectId] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class DailyCardBase(BaseModel):
    """每日卡片基本信息"""
    date: date = Field(default_factory=lambda: datetime.utcnow().date())
    tasks: List[CardTask] = Field(default_factory=list)
    accomplishments: List[Accomplishment] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True

class DailyCardCreate(DailyCardBase):
    """创建每日卡片时的数据模型"""
    pass

class DailyCardUpdate(BaseModel):
    """更新每日卡片时的数据模型"""
    tasks: Optional[List[CardTask]] = None
    accomplishments: Optional[List[Accomplishment]] = None

class DailyCardInDB(DailyCardBase):
    """数据库中的每日卡片模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class DailyCard(DailyCardInDB):
    """API响应中的每日卡片模型"""
    pass
