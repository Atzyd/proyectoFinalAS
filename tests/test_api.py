# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app, state

client = TestClient(app)

def test_full_game_correct_secret():
    # iniciar con secret conocido
    r = client.post("/start", json={"max": 10, "secret": 7})
    assert r.status_code == 200

    r = client.get("/status", params={"show_secret": True})
    assert r.status_code == 200
    assert r.json()["secret"] == 7

    r = client.get("/guess", params={"number": 5})
    assert r.json()["result"] == "bajo"
    assert r.json()["attempts"] == 1

    r = client.get("/guess", params={"number": 9})
    assert r.json()["result"] == "alto"
    assert r.json()["attempts"] == 2

    r = client.get("/guess", params={"number": 7})
    assert r.json()["result"] == "correcto"
    assert r.json()["attempts"] == 3

def test_guess_without_start():
    # reiniciamos el estado manualmente para simular no iniciado
    state["started"] = False
    state["secret"] = None
    r = client.get("/guess", params={"number": 1})
    assert r.status_code == 400
