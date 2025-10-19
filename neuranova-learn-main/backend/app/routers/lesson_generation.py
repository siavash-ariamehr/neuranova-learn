from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Lesson, Subject, Difficulty, AgeRange
from app.auth import get_current_user
from app.services.lesson_generator import lesson_generator
from pydantic import BaseModel

router = APIRouter(prefix="/api/lesson-generation", tags=["lesson-generation"])

class LessonGenerateRequest(BaseModel):
    subject: Subject
    difficulty: Difficulty
    age_range: AgeRange
    language: str = "en"

@router.post("/generate")
async def generate_lesson(
    request: LessonGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        lesson_data = await lesson_generator.generate_with_gpt4o(
            subject=request.subject,
            difficulty=request.difficulty,
            age_range=request.age_range,
            language=request.language
        )
        
        db_lesson = Lesson(**lesson_data)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        
        return db_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")

@router.get("/import-oer")
async def import_oer_commons(
    subject: str = "science",
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        oer_lessons = await lesson_generator.import_from_oer_commons(subject, limit)
        imported_count = 0
        
        for oer_lesson in oer_lessons:
            db_lesson = Lesson(
                title=oer_lesson.get("title", f"{subject} Lesson"),
                content=oer_lesson.get("description", "Imported from OER Commons"),
                subject=Subject.SCIENCE,
                difficulty=Difficulty.INTERMEDIATE,
                age_range=AgeRange.HIGH_SCHOOL,
                language="en",
                source="OER Commons"
            )
            db.add(db_lesson)
            imported_count += 1
        
        db.commit()
        return {"imported": imported_count, "source": "OER Commons"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import from OER Commons: {str(e)}")
