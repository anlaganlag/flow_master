from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from bson import ObjectId

from app.core.config import settings
from app.core.db import get_collection
from app.schemas.token import TokenPayload
from app.schemas.user import UserInDB

# OAuth2密码流的令牌URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    获取当前用户
    
    Args:
        token: JWT令牌
        
    Returns:
        当前用户对象
        
    Raises:
        HTTPException: 如果令牌无效或用户不存在
    """
    try:
        # 解码JWT令牌
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从数据库获取用户
    user_collection = get_collection("users")
    user = await user_collection.find_one({"_id": ObjectId(token_data.sub)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserInDB(**user)
