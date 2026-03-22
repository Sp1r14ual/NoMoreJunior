# backend/app/routers/questions.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud
from ..database import get_db
from ..dependencies import get_current_active_user, get_current_admin_user

router = APIRouter()

@router.get("/", response_model=List[schemas.QuestionOut])
def get_questions(
    category_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Получить список вопросов (с возможной фильтрацией по категории)"""
    questions = crud.get_questions(
        db, 
        category_id=category_id, 
        skip=offset, 
        limit=limit
    )
    return questions


@router.get("/random", response_model=List[schemas.QuestionOut])
def get_random_questions(
    category_id: int,
    count: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Получить случайные вопросы из указанной категории"""
    questions = crud.get_random_questions(db, category_id=category_id, count=count)
    # if len(questions) < count:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"В категории недостаточно вопросов (найдено только {len(questions)})"
    #     )
    return questions


@router.get("/{question_id}", response_model=schemas.QuestionOut)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    question = crud.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return question