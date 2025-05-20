from typing import Any, List
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.core.deps import get_current_user
from app.core.db import get_collection
from app.schemas.user import UserInDB
from app.schemas.daily_card import DailyCard, DailyCardCreate, DailyCardUpdate, AccomplishmentCreate, Accomplishment

router = APIRouter()

@router.get("", response_model=List[DailyCard])
async def read_daily_cards(
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    获取当前用户的所有每日卡片
    """
    card_collection = get_collection("daily_cards")
    
    # 查询卡片
    cards = await card_collection.find({
        "user_id": ObjectId(current_user.id)
    }).sort("date", -1).to_list(length=30)  # 最近30张卡片
    
    return cards

@router.get("/today", response_model=DailyCard)
async def read_today_card(
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    获取今天的卡片
    """
    card_collection = get_collection("daily_cards")
    
    # 获取今天的日期
    today = datetime.utcnow().date()
    
    # 查询今天的卡片
    card = await card_collection.find_one({
        "user_id": ObjectId(current_user.id),
        "date": today
    })
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="今天的卡片不存在"
        )
    
    return card

@router.post("", response_model=DailyCard, status_code=status.HTTP_201_CREATED)
async def create_daily_card(
    card_in: DailyCardCreate,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    创建新的每日卡片
    """
    card_collection = get_collection("daily_cards")
    task_collection = get_collection("tasks")
    
    # 设置日期，如果未提供则使用今天的日期
    card_date = card_in.date or datetime.utcnow().date()
    
    # 检查该日期是否已存在卡片
    existing_card = await card_collection.find_one({
        "user_id": ObjectId(current_user.id),
        "date": card_date
    })
    
    if existing_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该日期 ({card_date}) 的卡片已存在"
        )
    
    # 验证任务数量
    if len(card_in.tasks) < 1 or len(card_in.tasks) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="每日卡片应包含1-5个任务"
        )
    
    # 验证任务是否存在并属于当前用户
    tasks_data = []
    for task_item in card_in.tasks:
        task = await task_collection.find_one({
            "_id": ObjectId(task_item.task_id),
            "user_id": ObjectId(current_user.id)
        })
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"任务 {task_item.task_id} 不存在或不属于当前用户"
            )
        
        tasks_data.append({
            "task_id": ObjectId(task_item.task_id),
            "title": task_item.title or task["title"],
            "is_completed": task_item.is_completed
        })
    
    # 准备卡片数据
    now = datetime.utcnow()
    card_data = {
        "user_id": ObjectId(current_user.id),
        "date": card_date,
        "tasks": tasks_data,
        "accomplishments": [],
        "created_at": now,
        "updated_at": now
    }
    
    # 插入卡片
    result = await card_collection.insert_one(card_data)
    
    # 获取新创建的卡片
    new_card = await card_collection.find_one({"_id": result.inserted_id})
    
    return new_card

@router.put("/{card_id}", response_model=DailyCard)
async def update_daily_card(
    card_id: str,
    card_in: DailyCardUpdate,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    更新每日卡片
    """
    card_collection = get_collection("daily_cards")
    
    # 查询卡片
    card = await card_collection.find_one({
        "_id": ObjectId(card_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="卡片不存在"
        )
    
    # 准备更新数据
    update_data = {}
    if card_in.tasks is not None:
        # 验证任务数量
        if len(card_in.tasks) < 1 or len(card_in.tasks) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="每日卡片应包含1-5个任务"
            )
        
        # 转换任务数据
        tasks_data = []
        for task_item in card_in.tasks:
            tasks_data.append({
                "task_id": ObjectId(task_item.task_id),
                "title": task_item.title,
                "is_completed": task_item.is_completed
            })
        
        update_data["tasks"] = tasks_data
    
    update_data["updated_at"] = datetime.utcnow()
    
    # 更新卡片
    await card_collection.update_one(
        {"_id": ObjectId(card_id)},
        {"$set": update_data}
    )
    
    # 获取更新后的卡片
    updated_card = await card_collection.find_one({"_id": ObjectId(card_id)})
    
    return updated_card

@router.post("/{card_id}/accomplishments", response_model=Accomplishment)
async def add_accomplishment(
    card_id: str,
    accomplishment_in: AccomplishmentCreate,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    添加成就到每日卡片
    """
    card_collection = get_collection("daily_cards")
    
    # 查询卡片
    card = await card_collection.find_one({
        "_id": ObjectId(card_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="卡片不存在"
        )
    
    # 准备成就数据
    accomplishment_data = accomplishment_in.dict()
    if accomplishment_data.get("task_id"):
        accomplishment_data["task_id"] = ObjectId(accomplishment_data["task_id"])
    
    # 更新卡片
    await card_collection.update_one(
        {"_id": ObjectId(card_id)},
        {
            "$push": {"accomplishments": accomplishment_data},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return accomplishment_data
