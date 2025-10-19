from fastapi import APIRouter, UploadFile, File, Depends
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api/voice", tags=["voice"])

@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    return {
        "text": "Sample transcription (Whisper integration pending)",
        "language": "en",
        "confidence": 0.95
    }

@router.post("/detect-accent")
async def detect_accent(
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    return {
        "accent": "neutral",
        "confidence": 0.85,
        "suggestions": []
    }
