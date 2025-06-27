from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_logic import extraer_datos_con_ia, procesar_datos

app = FastAPI()

class DatosUsuario(BaseModel):
    nombre: str
    cedula: str
    tipo_contrato: str
    salario: float

class TextoLibre(BaseModel):
    mensaje: str

@app.post("/analizar-mensaje")
def analizar_mensaje(texto: TextoLibre):
    try:
        datos_extraidos = extraer_datos_con_ia(texto.mensaje)

        datos_validados = procesar_datos(DatosUsuario(**datos_extraidos))

        return {
            "mensaje": "Datos extraídos y validados correctamente.",
            "datos": datos_validados
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
