# backend/app/models/category.py
from sqlalchemy import Column, Integer, String, Text
from ..database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # можно добавить:
    # created_at = Column(DateTime, server_default=func.now())
    # is_active = Column(Boolean, default=True)