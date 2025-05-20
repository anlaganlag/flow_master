from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.core.deps import get_current_user
from app.core.db import get_collection
from app.schemas.user import UserInDB
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()

@router.get("", response_model=List[Task])
async def read_tasks(
    list_type: str = None,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    获取当前用户的任务列表
    """
    task_collection = get_collection("tasks")
    
    # 构建查询条件
    query = {"user_id": ObjectId(current_user.id)}
    if list_type:
        query["list_type"] = list_type
    
    # 查询任务
    tasks = await task_collection.find(query).to_list(length=100)
    
    return tasks

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    创建新任务
    """
    task_collection = get_collection("tasks")
    
    # 准备任务数据
    task_data = task_in.dict()
    task_data["user_id"] = ObjectId(current_user.id)
    task_data["is_completed"] = False
    task_data["created_at"] = datetime.utcnow()
    task_data["updated_at"] = datetime.utcnow()
    
    # 插入任务
    result = await task_collection.insert_one(task_data)
    
    # 获取新创建的任务
    new_task = await task_collection.find_one({"_id": result.inserted_id})
    
    return new_task

@router.get("/{task_id}", response_model=Task)
async def read_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    获取特定任务
    """
    task_collection = get_collection("tasks")
    
    # 查询任务
    task = await task_collection.find_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_in: TaskUpdate,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    更新任务
    """
    task_collection = get_collection("tasks")
    
    # 查询任务
    task = await task_collection.find_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    # 准备更新数据
    update_data = task_in.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    # 如果任务被标记为完成，设置完成时间
    if "is_completed" in update_data and update_data["is_completed"] and not task.get("is_completed"):
        update_data["completed_at"] = datetime.utcnow()
    
    # 更新任务
    await task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    
    # 获取更新后的任务
    updated_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    删除任务
    """
    task_collection = get_collection("tasks")
    
    # 查询任务
    task = await task_collection.find_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    # 删除任务
    await task_collection.delete_one({"_id": ObjectId(task_id)})
    
    return None

@router.put("/{task_id}/complete", response_model=Task)
async def complete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    将任务标记为完成
    """
    task_collection = get_collection("tasks")
    
    # 查询任务
    task = await task_collection.find_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    # 更新任务
    now = datetime.utcnow()
    await task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {
            "is_completed": True,
            "completed_at": now,
            "updated_at": now
        }}
    )
    
    # 获取更新后的任务
    updated_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    
    return updated_task

@router.put("/{task_id}/move", response_model=Task)
async def move_task(
    task_id: str,
    list_type: str,
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    将任务移动到不同的列表
    """
    task_collection = get_collection("tasks")
    
    # 验证列表类型
    valid_list_types = ["todo", "watch", "later"]
    if list_type not in valid_list_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的列表类型。有效类型: {', '.join(valid_list_types)}"
        )
    
    # 查询任务
    task = await task_collection.find_one({
        "_id": ObjectId(task_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    # 更新任务
    now = datetime.utcnow()
    await task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {
            "list_type": list_type,
            "updated_at": now
        }}
    )
    
    # 获取更新后的任务
    updated_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    
    return updated_task
