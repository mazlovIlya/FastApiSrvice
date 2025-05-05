from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.database import SessionLocal, engine, Base
import pytest
from datetime import date
import time

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    # Создаем таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    yield
    # Очищаем таблицы после теста
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def unique_email():
    return f"test_{int(time.time())}@example.com"

def test_create_user(setup_database, unique_email):
    response = client.post("/users/", json={
        "email": unique_email,
        "password": "password123",
        "created_at": "2023-09-01"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email

def test_get_user(setup_database, unique_email):
    # Сначала создаем пользователя
    client.post("/users/", json={
        "email": unique_email,
        "password": "password123",
        "created_at": "2023-09-01"
    })
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email

def test_update_user(setup_database, unique_email):
    # Сначала создаем пользователя
    client.post("/users/", json={
        "email": unique_email,
        "password": "password123",
        "created_at": "2023-09-01"
    })
    new_email = f"updated_{int(time.time())}@example.com"
    response = client.put("/users/1", json={
        "email": new_email,
        "password": "newpassword",
        "created_at": "2023-09-01"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_email

def test_delete_user(setup_database, unique_email):
    # Сначала создаем пользователя
    client.post("/users/", json={
        "email": unique_email,
        "password": "password123",
        "created_at": "2023-09-01"
    })
    response = client.delete("/users/1")
    assert response.status_code == 204