from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from agent_logic import procesar_datos


app = FastAPI()

class DatosUsuario(BaseModel):
    nombre: str
    num_id: str
    tipo_contrato: str

@app.post("/generate-contract")
def generate_contract(datos: DatosUsuario):
    try:
        datos_procesados = procesar_datos(datos)
        print(" = > Datos listos para backend:", datos_procesados)

        return {
            "message": "Datos validados y listos para generar el contrato.",
            "datos": datos_procesados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
