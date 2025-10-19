import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    import random
    email = f"trans{random.randint(1000,9999)}@test.com"
    client.post("/api/auth/register", json={"email": email, "password": "pass123", "role": "student"})
    response = client.post("/api/auth/token", data={"username": email, "password": "pass123"})
    return response.json()["access_token"]

def test_supported_languages():
    response = client.get("/api/translation/supported-languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert "count" in data
    languages = data["languages"]
    assert "en" in languages
    assert "hu" in languages
    assert "bg" in languages
    assert "el" in languages
    assert data["count"] == 24

def test_translate_text():
    token = get_auth_token()
    response = client.post(
        "/api/translation/translate",
        headers={"Authorization": f"Bearer {token}"},
        json={"text": "Hello world", "source_lang": "en", "target_lang": "es"}
    )
    assert response.status_code == 200
    assert "translated_text" in response.json()
