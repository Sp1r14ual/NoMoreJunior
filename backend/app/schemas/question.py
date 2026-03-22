# backend/app/schemas/question.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class QuestionBase(BaseModel):
    text: str = Field(..., min_length=10)
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: Literal["A", "B", "C", "D"]
    explanation: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class QuestionCreate(QuestionBase):
    category_id: int


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_option: Optional[Literal["A", "B", "C", "D"]] = None
    explanation: Optional[str] = None
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None
    category_id: Optional[int] = None


class QuestionOut(QuestionBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True


class QuestionShort(BaseModel):
    id: int
    text: str
    difficulty: str

    class Config:
        from_attributes = True