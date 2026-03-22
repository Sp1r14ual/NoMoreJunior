# backend/app/crud/question.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas


def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_questions(
    db: Session,
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Question)
    if category_id:
        query = query.filter(models.Question.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def get_random_questions(
    db: Session,
    category_id: int,
    count: int = 10
) -> List[models.Question]:
    return (
        db.query(models.Question)
        .filter(models.Question.category_id == category_id)
        .order_by(func.random())
        .limit(count)
        .all()
    )


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(
    db: Session,
    question_id: int,
    question_update: schemas.QuestionUpdate
):
    db_question = get_question(db, question_id)
    if not db_question:
        return None
    
    update_data = question_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int):
    db_question = get_question(db, question_id)
    if not db_question:
        return False
    
    db.delete(db_question)
    db.commit()
    return True