import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
from app import models, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Erstellen Sie eine Testdatenbank
Base.metadata.create_all(bind=engine)

# Dependency Override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_item(test_db):
    response = client.post("/items/", json={"name": "Test Item", "description": "This is a test item"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert "id" in data

def test_read_items(test_db):
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_item(test_db):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"

def test_update_item(test_db):
    response = client.put("/items/1", json={"name": "Updated Test Item", "description": "This is an updated test item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Test Item"
    assert data["description"] == "This is an updated test item"

def test_delete_item(test_db):
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Test Item"
    assert data["description"] == "This is an updated test item"
