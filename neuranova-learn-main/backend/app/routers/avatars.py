from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Avatar, User
from app.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/avatars", tags=["avatars"])

class AvatarResponse(BaseModel):
    id: int
    user_id: int
    model_type: str
    customization_data: dict
    
    class Config:
        from_attributes = True

@router.get("/models")
async def list_avatar_models():
    models = [
        {"id": 1, "name": "Professional Male 1", "has_hijab": False},
        {"id": 2, "name": "Professional Female 1", "has_hijab": False},
        {"id": 3, "name": "Professional Female 2 (Hijab)", "has_hijab": True},
        {"id": 4, "name": "Professional Male 2", "has_hijab": False},
        {"id": 5, "name": "Professional Female 3 (Hijab)", "has_hijab": True},
        {"id": 6, "name": "Student Male 1", "has_hijab": False},
        {"id": 7, "name": "Student Female 1", "has_hijab": False},
        {"id": 8, "name": "Student Female 2 (Hijab)", "has_hijab": True},
        {"id": 9, "name": "Teacher Male 1", "has_hijab": False},
        {"id": 10, "name": "Teacher Female 1 (Hijab)", "has_hijab": True},
    ]
    return {"models": models}

@router.get("/user/{user_id}", response_model=AvatarResponse)
async def get_user_avatar(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    avatar = db.query(Avatar).filter(Avatar.user_id == user_id).first()
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return avatar

@router.post("/generate-lipsync")
async def generate_lipsync(
    text: str,
    avatar_id: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "status": "pending",
        "message": "Lip-sync generation queued. This feature requires GPU processing and will be implemented in production.",
        "video_url": None
    }
