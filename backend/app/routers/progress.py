from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Progress, User
from app.schemas import ProgressCreate, ProgressResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.post("", response_model=ProgressResponse)
async def update_progress(
    progress: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.lesson_id == progress.lesson_id
    ).first()
    
    if db_progress:
        for key, value in progress.model_dump(exclude_unset=True).items():
            setattr(db_progress, key, value)
    else:
        db_progress = Progress(
            user_id=current_user.id,
            **progress.model_dump()
        )
        db.add(db_progress)
    
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.get("/{user_id}", response_model=List[ProgressResponse])
async def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role.value not in ["teacher", "parent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this progress")
    
    progress_list = db.query(Progress).filter(Progress.user_id == user_id).all()
    return progress_list
