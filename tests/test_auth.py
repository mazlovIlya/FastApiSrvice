from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.database import SessionLocal, engine, Base
import pytest
from datetime import date

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_user(setup_database):
    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "password123",
        "created_at": "2023-09-01"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

def test_login(setup_database):
    # Регистрируем пользователя
    client.post("/register", json={
        "email": "test@example.com",
        "password": "password123",
        "created_at": "2023-09-01"
    })
    # Логинимся
    response = client.post("/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"