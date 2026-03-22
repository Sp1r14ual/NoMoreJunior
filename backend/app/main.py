from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, questions, progress, admin, categories

Base.metadata.create_all(bind=engine)  # для dev, потом alembic

app = FastAPI(title="NoMoreJunior API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # потом поменяешь на домен фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(categories.router)