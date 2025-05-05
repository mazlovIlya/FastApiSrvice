from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL базы данных (по умолчанию SQLite для локальной разработки)
# Для PostgreSQL/MySQL замените на соответствующий URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"

# Настройка движка SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Фабрика сессий для работы с ORM
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """
    Зависимость для получения сессии базы данных.
    Используется в FastAPI маршрутах через Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()