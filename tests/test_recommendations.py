from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Category, Transaction
from app.database import SessionLocal, engine, Base
import pytest
from datetime import date, timedelta

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Добавляем пользователя
    user = User(email="user@example.com", hashed_password="pass", created_at=date(2023, 9, 1))
    db.add(user)
    db.commit()
    db.refresh(user)  # Обновляем, чтобы получить user.id
    
    # Добавляем категорию
    category = Category(name="Food", owner=user)
    db.add(category)
    db.commit()  # Сохраняем категорию
    db.refresh(category)  # Обновляем, чтобы получить category.id
    
    # Добавляем транзакцию за последние 90 дней
    today = date.today()
    transaction = Transaction(
        amount=20000.0,
        type="expense",
        date=today - timedelta(days=60),  # Убедитесь, что дата в пределах 90 дней
        category_id=category.id,
        user_id=user.id
    )
    db.add(transaction)
    db.commit()  # Сохраняем транзакцию
    db.refresh(transaction)
    
    yield
    # Очищаем таблицы
    Base.metadata.drop_all(bind=engine)

def test_get_recommendations(setup_database):
    db = SessionLocal()
    user = db.query(User).first()
    response = client.get(f"/recommendations/?user_id={user.id}")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) >= 0