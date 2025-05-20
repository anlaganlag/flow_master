from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.deps import get_current_user
from app.core.db import get_collection
from app.schemas.token import Token
from app.schemas.user import User, UserCreate, UserInDB

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate) -> Any:
    """
    注册新用户
    """
    user_collection = get_collection("users")
    
    # 检查邮箱是否已存在
    if await user_collection.find_one({"email": user_in.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 检查用户名是否已存在
    if await user_collection.find_one({"username": user_in.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用"
        )
    
    # 创建新用户
    user_data = user_in.dict()
    user_data["password"] = get_password_hash(user_in.password)
    
    result = await user_collection.insert_one(user_data)
    
    # 获取新创建的用户
    new_user = await user_collection.find_one({"_id": result.inserted_id})
    
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 兼容的令牌登录，获取访问令牌
    """
    user_collection = get_collection("users")
    
    # 查找用户
    user = await user_collection.find_one({"email": form_data.username})
    if not user:
        # 尝试使用用户名查找
        user = await user_collection.find_one({"username": form_data.username})
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱/用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 更新最后登录时间
    from datetime import datetime
    await user_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user["_id"]), expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)) -> Any:
    """
    获取当前用户信息
    """
    return current_user
