from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import UserRole, Subject, Difficulty, AgeRange

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.STUDENT
    age: Optional[int] = None
    skill_level: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    language: str = "en"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LessonBase(BaseModel):
    title: str
    content: str
    subject: Subject
    difficulty: Difficulty
    age_range: AgeRange
    language: str = "en"
    source: Optional[str] = None
    ar_vr_content: Optional[Dict[str, Any]] = None
    interactive_elements: Optional[Dict[str, Any]] = None

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProgressBase(BaseModel):
    lesson_id: int
    completion_percentage: float = 0.0
    score: Optional[float] = None
    time_spent: Optional[int] = None
    ai_feedback: Optional[Dict[str, Any]] = None

class ProgressCreate(ProgressBase):
    pass

class ProgressResponse(ProgressBase):
    id: int
    user_id: int
    last_accessed: datetime
    
    class Config:
        from_attributes = True

class NFTRewardBase(BaseModel):
    token_id: str
    contract_address: Optional[str] = None
    nft_metadata: Optional[Dict[str, Any]] = None
    achievement_type: str

class NFTRewardCreate(NFTRewardBase):
    pass

class NFTRewardResponse(NFTRewardBase):
    id: int
    user_id: int
    minted_at: datetime
    
    class Config:
        from_attributes = True

class AvatarBase(BaseModel):
    model_url: Optional[str] = None
    customization_data: Optional[Dict[str, Any]] = None
    has_hijab: bool = False

class AvatarCreate(AvatarBase):
    pass

class AvatarResponse(AvatarBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
