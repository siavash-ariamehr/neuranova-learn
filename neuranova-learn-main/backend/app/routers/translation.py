from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.models import User
from app.auth import get_current_user
from app.services.translation_service import translation_service

router = APIRouter(prefix="/api/translation", tags=["translation"])

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str

class BatchTranslateRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        translated = await translation_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.post("/batch-translate")
async def batch_translate_texts(
    request: BatchTranslateRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        translations = await translation_service.batch_translate(
            texts=request.texts,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return {
            "translations": translations,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")

@router.post("/detect-language")
async def detect_language(
    text: str,
    current_user: User = Depends(get_current_user)
):
    try:
        detected_lang = await translation_service.detect_language(text)
        return {"text": text, "detected_language": detected_lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")

@router.get("/supported-languages")
async def get_supported_languages():
    return {
        "languages": translation_service.supported_languages,
        "count": len(translation_service.supported_languages)
    }
