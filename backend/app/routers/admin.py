# backend/app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_admin_user

router = APIRouter()

# ────────────────────────────────────────────────
# Категории
# ────────────────────────────────────────────────

@router.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    existing = crud.get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(400, "Категория с таким названием уже существует")
    
    return crud.create_category(db, category)


@router.get("/categories", response_model=List[schemas.CategoryOut])
def get_all_categories(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    return crud.get_categories(db)


# ────────────────────────────────────────────────
# Вопросы
# ────────────────────────────────────────────────

@router.post("/questions", response_model=schemas.QuestionOut, status_code=201)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    category = crud.get_category(db, question.category_id)
    if not category:
        raise HTTPException(404, "Категория не найдена")
    
    return crud.create_question(db, question)


@router.put("/questions/{question_id}", response_model=schemas.QuestionOut)
def update_question(
    question_id: int,
    question_update: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    question = crud.update_question(db, question_id, question_update)
    if not question:
        raise HTTPException(404, "Вопрос не найден")
    return question


@router.delete("/questions/{question_id}", status_code=204)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    success = crud.delete_question(db, question_id)
    if not success:
        raise HTTPException(404, "Вопрос не найден")
    return None

@router.get("/users", response_model=List[schemas.UserListItem])
def get_users_list(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user),
    
    # параметры для фильтрации и пагинации
    skip: int = Query(0, ge=0, description="Пропустить N записей"),
    limit: int = Query(50, ge=1, le=200, description="Количество записей на странице"),
    only_active: bool = Query(False, description="Показывать только активных пользователей"),
    search: Optional[str] = Query(None, description="Поиск по username или email (частичное совпадение)")
):
    """
    Получить список пользователей  
    Доступно только администраторам
    """
    users = crud.user.get_users(
        db=db,
        skip=skip,
        limit=limit,
        only_active=only_active,
        search=search
    )
    
    return users