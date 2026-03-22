# backend/app/routers/progress.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter()

@router.post("/submit-answer", response_model=schemas.ProgressUpdateResponse)
def submit_answer(
    answer: schemas.AnswerSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Отправить ответ на вопрос и обновить прогресс пользователя
    """
    question = crud.get_question(db, answer.question_id)
    if not question:
        raise HTTPException(404, "Вопрос не найден")

    is_correct = (answer.selected_option == question.correct_option)

    # Обновляем или создаём запись прогресса по категории
    progress = crud.get_or_create_progress(
        db,
        user_id=current_user.id,
        category_id=question.category_id
    )

    progress.total_questions += 1
    if is_correct:
        progress.score += 1

    db.commit()
    db.refresh(progress)

    return schemas.ProgressUpdateResponse(
        question_id=answer.question_id,
        is_correct=is_correct,
        current_score=progress.score,
        total_attempts=progress.total_questions,
        accuracy=round((progress.score / progress.total_questions) * 100, 1) if progress.total_questions > 0 else 0.0
    )


# @router.get("/me", response_model=List[schemas.ProgressOut])
@router.get("/me")
def get_my_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Получить весь прогресс текущего пользователя"""
    progress_list = crud.get_user_progress(db, user_id=current_user.id)
    return progress_list