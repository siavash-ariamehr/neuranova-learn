from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import CollaborationSession, User
from app.auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
import os
import time

router = APIRouter(prefix="/api/collaboration", tags=["collaboration"])

class SessionCreate(BaseModel):
    participants: List[int]

class SessionResponse(BaseModel):
    id: int
    participants: List[int]
    agora_channel_name: str
    agora_token: str
    start_time: datetime
    active: bool
    
    class Config:
        from_attributes = True

@router.post("/session", response_model=SessionResponse)
async def create_collaboration_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id not in session_data.participants:
        session_data.participants.append(current_user.id)
    
    channel_name = f"neuranova_{int(time.time())}_{current_user.id}"
    
    agora_token = generate_agora_token(channel_name, current_user.id)
    
    db_session = CollaborationSession(
        participants=session_data.participants,
        agora_channel_name=channel_name,
        active=True
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return SessionResponse(
        id=db_session.id,
        participants=db_session.participants,
        agora_channel_name=channel_name,
        agora_token=agora_token,
        start_time=db_session.start_time,
        active=db_session.active
    )

@router.get("/session/{session_id}")
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(CollaborationSession).filter(
        CollaborationSession.id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if current_user.id not in session.participants:
        raise HTTPException(status_code=403, detail="Not authorized to access this session")
    
    agora_token = generate_agora_token(session.agora_channel_name, current_user.id)
    
    return {
        "id": session.id,
        "participants": session.participants,
        "agora_channel_name": session.agora_channel_name,
        "agora_token": agora_token,
        "start_time": session.start_time,
        "active": session.active
    }

def generate_agora_token(channel_name: str, user_id: int) -> str:
    app_id = os.getenv("AGORA_APP_ID", "")
    app_certificate = os.getenv("AGORA_APP_CERTIFICATE", "")
    
    if not app_id or not app_certificate:
        return "demo_token_configure_agora_credentials"
    
    uid = user_id
    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds
    
    return f"temp_token_{channel_name}_{uid}_{privilege_expired_ts}"
