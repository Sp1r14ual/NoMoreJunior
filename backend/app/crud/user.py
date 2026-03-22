# backend/app/crud/user.py
from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.security import get_password_hash
from typing import List


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = False,
    search: str | None = None
) -> List[models.User]:
    query = db.query(models.User)
    
    if only_active:
        query = query.filter(models.User.is_active == True)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                models.User.username.ilike(search),
                models.User.email.ilike(search)
            )
        )
    
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool = None,
    is_admin: bool = None
):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    if is_active is not None:
        db_user.is_active = is_active
    if is_admin is not None:
        db_user.is_admin = is_admin
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True