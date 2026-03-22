# backend/app/models/progress.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )
    
    score = Column(Integer, default=0, nullable=False)               # количество правильных ответов
    total_questions = Column(Integer, default=0, nullable=False)     # сколько вопросов пройдено
    
    last_attempt_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        # один прогресс на пару пользователь-категория
        {"sqlite_autoincrement": True},
    )