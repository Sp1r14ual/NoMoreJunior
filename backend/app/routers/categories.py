# backend/app/routers/categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


# ────────────────────────────────────────────────
# Публичные эндпоинты (доступны всем авторизованным пользователям)
# ────────────────────────────────────────────────

@router.get("/", response_model=List[schemas.CategoryOut])
def get_all_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """Получить список всех категорий"""
    categories = crud.category.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=schemas.CategoryOut)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Получить одну категорию по ID"""
    category = crud.category.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


# ────────────────────────────────────────────────
# Админские эндпоинты (только для администраторов)
# ────────────────────────────────────────────────

@router.post("/", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    """Создать новую категорию (только админ)"""
    if crud.category.get_category_by_name(db, category_in.name):
        raise HTTPException(
            status_code=400,
            detail="Категория с таким названием уже существует"
        )
    
    return crud.category.create_category(db, category_in)


@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    category_in: schemas.CategoryCreate,  # или CategoryUpdate, если сделаешь частичное обновление
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    """Обновить категорию (только админ)"""
    updated = crud.category.update_category(db, category_id, category_in)
    if updated is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    """Удалить категорию (только админ)"""
    if not crud.category.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return None