from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """用户基本信息"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None

class UserCreate(UserBase):
    """创建用户请求模型"""
    email: EmailStr
    username: str
    password: str

class UserUpdate(UserBase):
    """更新用户请求模型"""
    password: Optional[str] = None

class UserInDBBase(UserBase):
    """数据库中的用户模型基类"""
    id: str

    class Config:
        orm_mode = True

class UserInDB(UserInDBBase):
    """数据库中的用户模型（包含密码哈希）"""
    password: str

class User(UserInDBBase):
    """API响应中的用户模型（不包含密码）"""
    pass
