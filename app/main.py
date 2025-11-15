# app/main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import random
from typing import Optional

app = FastAPI(title="Adivina el Número - API")

class StartRequest(BaseModel):
    max: Optional[int] = 100
    secret: Optional[int] = None  # opcional, para pruebas

# Estado en memoria (se pierde si se reinicia el contenedor)
state = {
    "started": False,
    "secret": None,
    "max": 100,
    "attempts": 0,
    "last_guess": None,
}

@app.post("/start")
def start_game(payload: StartRequest):
    if payload.max is None or payload.max < 1:
        raise HTTPException(status_code=400, detail="max debe ser >= 1")
    state["max"] = int(payload.max)
    if payload.secret is not None:
        if not (0 <= payload.secret <= state["max"]):
            raise HTTPException(status_code=400, detail="secret fuera de rango")
        state["secret"] = int(payload.secret)
    else:
        state["secret"] = random.randint(0, state["max"])
    state["started"] = True
    state["attempts"] = 0
    state["last_guess"] = None
    return {"message": "Juego iniciado", "max": state["max"]}

@app.get("/guess")
def guess(number: int = Query(..., ge=0)):
    if not state["started"] or state["secret"] is None:
        raise HTTPException(status_code=400, detail="Juego no iniciado. Llama a POST /start")
    if number < 0 or number > state["max"]:
        raise HTTPException(status_code=400, detail=f"Number debe estar entre 0 y {state['max']}")
    state["attempts"] += 1
    state["last_guess"] = number
    secret = state["secret"]
    if number > secret:
        result = "Muy frio"
    elif number < secret:
        result = "bajo"
    else:
        result = "correcto"
        # opcional: terminar el juego después de acertar
        state["started"] = False
    return {
        "result": result,
        "attempts": state["attempts"],
        "last_guess": state["last_guess"]
    }

@app.get("/status")
def status(show_secret: Optional[bool] = Query(False)):
    # show_secret permite ver el numero secreto solo si lo pides (útil para pruebas)
    resp = {
        "started": state["started"],
        "max": state["max"],
        "attempts": state["attempts"],
        "last_guess": state["last_guess"],
    }
    if show_secret:
        resp["secret"] = state["secret"]
    return resp

@app.get("/")
def root():
    return {"message": "Adivina el Número - API. Usa /start, /guess y /status"}
