# backend/app/schemas/progress.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProgressBase(BaseModel):
    score: int = 0
    total_questions: int = 0


class ProgressOut(ProgressBase):
    id: int
    user_id: int
    category_id: int
    last_updated: datetime
    accuracy: float = 0.0  # можно вычислять на фронте или здесь

    class Config:
        from_attributes = True


class ProgressUpdateResponse(BaseModel):
    question_id: int
    is_correct: bool
    current_score: int
    total_attempts: int
    accuracy: float