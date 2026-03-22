# backend/app/schemas/answer.py
from pydantic import BaseModel
from typing import Literal


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: Literal["A", "B", "C", "D"]