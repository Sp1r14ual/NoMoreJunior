# backend/app/models/question.py
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )
    
    text = Column(Text, nullable=False)
    
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    
    correct_option = Column(
        String(1),
        nullable=False
    )  # 'A', 'B', 'C', 'D'
    
    explanation = Column(Text, nullable=True)
    # difficulty = Column(
    #     Enum(DifficultyLevel),
    #     default=DifficultyLevel.MEDIUM,
    #     nullable=False
    # )
    difficulty = Column(Text, nullable=False)
    
    # связи
    # category = relationship("Category", back_populates="questions")
    # category = relationship("Category", back_populates="questions")
    # questions = relationship("Question", back_populates="category", cascade="all, delete-orphan")