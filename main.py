from fastapi import FastAPI
from pydantic import BaseModel
from agent_logic import analizar_mensaje

app = FastAPI()

class InputMensaje(BaseModel):
    user_id: str
    mensaje: str

@app.post("/conversar")
def conversar(input: InputMensaje):
    respuesta = analizar_mensaje(input.user_id, input.mensaje)
    return {"respuesta": respuesta}
