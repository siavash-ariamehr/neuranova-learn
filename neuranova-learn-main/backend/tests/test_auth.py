import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    import random
    email = f"test{random.randint(1000,9999)}@example.com"
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "testpassword123",
            "role": "student"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == email

def test_login_user():
    import random
    email = f"login{random.randint(1000,9999)}@example.com"
    client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "testpass123",
            "role": "student"
        }
    )
    
    response = client.post(
        "/api/auth/token",
        data={
            "username": email,
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
