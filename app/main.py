from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, database

from app.routers import (
    auth,
    users,
    transactions,
    recommendations
)

app = FastAPI(
    title="Personal Finance Manager",
    description="API для управления личными финансами и генерации рекомендаций по оптимизации расходов."
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(recommendations.router)
app.include_router(auth.router)

# Инициализация базы данных
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Welcome to Personal Finance Manager API"}