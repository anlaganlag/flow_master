from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class CardTaskBase(BaseModel):
    """卡片任务基本信息"""
    task_id: str
    title: str
    is_completed: bool = False

class CardTask(CardTaskBase):
    """API中的卡片任务模型"""
    pass

class AccomplishmentBase(BaseModel):
    """成就基本信息"""
    title: str
    source: str
    task_id: Optional[str] = None

class AccomplishmentCreate(AccomplishmentBase):
    """创建成就请求模型"""
    pass

class Accomplishment(AccomplishmentBase):
    """API中的成就模型"""
    pass

class DailyCardBase(BaseModel):
    """每日卡片基本信息"""
    date: date
    tasks: List[CardTask] = []
    accomplishments: List[Accomplishment] = []

class DailyCardCreate(BaseModel):
    """创建每日卡片请求模型"""
    tasks: List[CardTaskBase]
    date: Optional[date] = None

class DailyCardUpdate(BaseModel):
    """更新每日卡片请求模型"""
    tasks: Optional[List[CardTaskBase]] = None

class DailyCardInDBBase(DailyCardBase):
    """数据库中的每日卡片模型基类"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DailyCard(DailyCardInDBBase):
    """API响应中的每日卡片模型"""
    pass
