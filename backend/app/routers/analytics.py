from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.models import User, Progress, Lesson
from app.auth import get_current_user
import os

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role.value not in ["teacher", "parent", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this analytics")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress_records = db.query(Progress).filter(Progress.user_id == user_id).all()
    
    total_lessons = len(progress_records)
    completed_lessons = sum(1 for p in progress_records if p.completion_percentage >= 100)
    average_score = sum(p.score for p in progress_records if p.score) / len(progress_records) if progress_records else 0
    total_time_spent = sum(p.time_spent for p in progress_records if p.time_spent)
    
    dropout_risk = calculate_dropout_risk(progress_records)
    
    recommended_lessons = await generate_recommendations(user, progress_records, db)
    
    return {
        "user_id": user_id,
        "total_lessons_started": total_lessons,
        "completed_lessons": completed_lessons,
        "average_score": round(average_score, 2),
        "total_time_spent_minutes": total_time_spent,
        "dropout_risk_percentage": round(dropout_risk * 100, 2),
        "recommended_lessons": recommended_lessons,
        "learning_path": await generate_learning_path(user, progress_records, db)
    }

def calculate_dropout_risk(progress_records: list) -> float:
    if not progress_records:
        return 0.5
    
    recent_activity = sum(1 for p in progress_records[-10:] if p.completion_percentage > 0)
    avg_completion = sum(p.completion_percentage for p in progress_records) / len(progress_records)
    
    dropout_risk = 1.0 - (recent_activity / 10.0 * 0.5 + avg_completion / 100.0 * 0.5)
    
    return max(0.0, min(1.0, dropout_risk))

async def generate_recommendations(user: User, progress_records: list, db: Session) -> list:
    completed_lesson_ids = [p.lesson_id for p in progress_records if p.completion_percentage >= 100]
    
    recommendations = db.query(Lesson).filter(
        Lesson.language == user.language,
        ~Lesson.id.in_(completed_lesson_ids)
    ).limit(5).all()
    
    return [{"id": l.id, "title": l.title, "subject": l.subject.value} for l in recommendations]

async def generate_learning_path(user: User, progress_records: list, db: Session) -> list:
    current_subjects = set(p.lesson.subject for p in progress_records if p.lesson)
    
    next_lessons = db.query(Lesson).filter(
        Lesson.language == user.language
    ).limit(10).all()
    
    return [{"id": l.id, "title": l.title, "subject": l.subject.value, "difficulty": l.difficulty.value} for l in next_lessons]
