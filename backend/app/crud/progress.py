# backend/app/crud/progress.py
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .. import models, schemas


def get_progress(
    db: Session,
    user_id: int,
    category_id: int
) -> Optional[models.UserProgress]:
    """Получить запись прогресса для конкретной категории пользователя"""
    return (
        db.query(models.UserProgress)
        .filter(
            and_(
                models.UserProgress.user_id == user_id,
                models.UserProgress.category_id == category_id
            )
        )
        .first()
    )


def get_or_create_progress(
    db: Session,
    user_id: int,
    category_id: int
) -> models.UserProgress:
    """Получить или создать запись прогресса"""
    progress = get_progress(db, user_id, category_id)
    if progress is None:
        progress = models.UserProgress(
            user_id=user_id,
            category_id=category_id,
            score=0,
            total_questions=0
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress


def update_progress(
    db: Session,
    user_id: int,
    category_id: int,
    is_correct: bool
) -> Tuple[models.UserProgress, bool]:
    """
    Обновить прогресс после ответа на вопрос.
    Возвращает (обновлённый объект, был_ли_ответ_правильным)
    """
    progress = get_or_create_progress(db, user_id, category_id)
    
    progress.total_questions += 1
    if is_correct:
        progress.score += 1
    
    db.commit()
    db.refresh(progress)
    
    return progress, is_correct


def get_user_progress(
    db: Session,
    user_id: int,
    category_id: Optional[int] = None
) -> List[models.UserProgress]:
    """Получить весь прогресс пользователя (по всем категориям или по одной)"""
    query = db.query(models.UserProgress).filter(models.UserProgress.user_id == user_id)
    if category_id is not None:
        query = query.filter(models.UserProgress.category_id == category_id)
    return query.order_by(models.UserProgress.last_attempt_at.desc()).all()


def reset_progress(
    db: Session,
    user_id: int,
    category_id: Optional[int] = None
) -> int:
    """Сбросить прогресс (для одной категории или для всех)"""
    query = db.query(models.UserProgress).filter(models.UserProgress.user_id == user_id)
    if category_id is not None:
        query = query.filter(models.UserProgress.category_id == category_id)
    
    deleted_count = query.delete()
    db.commit()
    return deleted_count