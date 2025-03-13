from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class AITranscriptions(Base):
    __tablename__ = 'ai_transcriptions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    transcription_data = Column(JSONB)
    created_at = Column(DateTime)