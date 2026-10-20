from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rewrite_endpoint():
    payload = {"text": "I need this now.", "style": "polite", "context": "chat"}
    response = client.post("/api/v1/rewrite", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "rewrite_options" in body
    assert len(body["rewrite_options"]) >= 3


def test_grammar_endpoint():
    payload = {"text": "He go to school yesterday."}
    response = client.post("/api/v1/grammar/check", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "corrected_text" in body
