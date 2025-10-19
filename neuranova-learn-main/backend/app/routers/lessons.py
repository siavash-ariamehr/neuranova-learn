from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Lesson, User, Subject, Difficulty, AgeRange
from app.schemas import LessonCreate, LessonResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/lessons", tags=["lessons"])

@router.get("", response_model=List[LessonResponse])
async def get_lessons(
    subject: Optional[Subject] = None,
    difficulty: Optional[Difficulty] = None,
    age_range: Optional[AgeRange] = None,
    language: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Lesson)
    
    if subject:
        query = query.filter(Lesson.subject == subject)
    if difficulty:
        query = query.filter(Lesson.difficulty == difficulty)
    if age_range:
        query = query.filter(Lesson.age_range == age_range)
    if language:
        query = query.filter(Lesson.language == language)
    
    lessons = query.offset(skip).limit(limit).all()
    return lessons

@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("", response_model=LessonResponse)
async def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_lesson = Lesson(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson
