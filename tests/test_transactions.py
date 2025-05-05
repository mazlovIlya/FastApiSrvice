from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Category
from app.database import SessionLocal, engine, Base
import pytest
from datetime import date

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Добавляем тестового пользователя и категорию
    user = User(email="user@example.com", hashed_password="pass", created_at=date(2023, 9, 1))
    category = Category(name="Food", owner=user)
    db.add(user)
    db.add(category)
    db.commit()
    db.refresh(user)
    db.refresh(category)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_transaction(setup_database):
    db = SessionLocal()
    user = db.query(User).first()
    category = db.query(Category).first()
    response = client.post("/transactions/", json={
        "amount": 100.0,
        "type": "expense",
        "date": "2023-09-01",
        "category_id": category.id,
        "user_id": user.id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.0

def test_get_transactions(setup_database):
    db = SessionLocal()
    user = db.query(User).first()
    transaction_data = {
        "amount": 50.0,
        "type": "income",
        "date": "2023-09-01",
        "category_id": 1,
        "user_id": user.id
    }
    client.post("/transactions/", json=transaction_data)
    response = client.get(f"/transactions/?user_id={user.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["amount"] == 50.0