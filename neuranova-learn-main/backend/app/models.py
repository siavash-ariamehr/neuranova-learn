from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMIN = "admin"

class Subject(str, enum.Enum):
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    ENGINEERING = "engineering"
    MATHEMATICS = "mathematics"
    BIOLOGY = "biology"
    CHEMISTRY = "chemistry"
    PHYSICS = "physics"

class Difficulty(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class AgeRange(str, enum.Enum):
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    VOCATIONAL = "vocational"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    age = Column(Integer)
    skill_level = Column(String)
    preferences = Column(JSON)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    progress = relationship("Progress", back_populates="user")
    nft_rewards = relationship("NFTReward", back_populates="user")
    avatar = relationship("Avatar", back_populates="user", uselist=False)

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    subject = Column(Enum(Subject), nullable=False, index=True)
    difficulty = Column(Enum(Difficulty), nullable=False, index=True)
    age_range = Column(Enum(AgeRange), nullable=False, index=True)
    language = Column(String, default="en", index=True)
    source = Column(String)
    ar_vr_content = Column(JSON)
    interactive_elements = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    progress = relationship("Progress", back_populates="lesson")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completion_percentage = Column(Float, default=0.0)
    score = Column(Float)
    time_spent = Column(Integer)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    ai_feedback = Column(JSON)
    
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")

class NFTReward(Base):
    __tablename__ = "nft_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_id = Column(String, unique=True)
    contract_address = Column(String)
    nft_metadata = Column(JSON)
    achievement_type = Column(String)
    minted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="nft_rewards")

class Avatar(Base):
    __tablename__ = "avatars"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    model_url = Column(String)
    customization_data = Column(JSON)
    has_hijab = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="avatar")

class CollaborationSession(Base):
    __tablename__ = "collaboration_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    participants = Column(JSON)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    chat_history = Column(JSON)
    agora_channel_name = Column(String)
    active = Column(Boolean, default=True)
