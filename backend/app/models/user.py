from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

class PyObjectId(ObjectId):
    """用于处理MongoDB ObjectId的自定义类型"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("无效的ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserBase(BaseModel):
    """用户基本信息"""
    email: EmailStr
    username: str
    
    class Config:
        arbitrary_types_allowed = True

class UserCreate(UserBase):
    """创建用户时的数据模型"""
    password: str

class UserUpdate(BaseModel):
    """更新用户时的数据模型"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class UserInDBBase(UserBase):
    """数据库中的用户模型基类"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class UserInDB(UserInDBBase):
    """数据库中的用户模型（包含密码哈希）"""
    password: str

class User(UserInDBBase):
    """API响应中的用户模型（不包含密码）"""
    pass
