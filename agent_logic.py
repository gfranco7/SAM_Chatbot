import json
import re
from openai import OpenAI
from dotenv import load_dotenv
import os
from session_store import *

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def procesar_datos(datos):
    nombre = datos.get("nombre", "").strip().title()
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        return False, "El nombre solo puede contener letras y espacios."

    cedula = datos.get("cedula", "").strip()
    if not (cedula.isdigit() and len(cedula) == 10):
        return False, "La cédula debe contener solo números y tener exactamente 10 dígitos."

    tipo_usuario = datos.get("tipo_contrato", "").strip().lower()

    tipos_validos = {
        "fijo": ["fijo", "temporal", "a termino fijo"],
        "indefinido": ["indefinido", "permanente", "a termino indefinido"],
        "prestacion": ["servicios", "freelance", "prestacion de servicios"]
    }

    tipo_contrato_estandar = None
    for clave, sinonimos in tipos_validos.items():
        if tipo_usuario in sinonimos:
            tipo_contrato_estandar = clave
            break

    if not tipo_contrato_estandar:
        return False, "El tipo de contrato no es reconocido."

    return True, {
        "nombre": nombre,
        "cedula": cedula,
        "tipo_contrato": tipo_contrato_estandar
    }


def extraer_datos_ia(mensaje):
    prompt = f"""
Devuelve un JSON con estos campos si están presentes: nombre, cedula, tipo_contrato. 
Esta informacion puede ser enviada por el usuario en un mensaje largo o con 
contxto adicional y en desorden. 
Por ejemplo:
Quiero un contrato de presatación de servicios para Maryana Peñaloza con 
numero de cedula 1103499169.

Si faltan o son inválidos, responde así: {{"error": "Descripción del problema"}}

Ejemplo válido:
{{
  "nombre": "Laura Pérez",
  "cedula": "1234567890",
  "tipo_contrato": "fijo"
}}

Texto:
\"\"\"{mensaje}\"\"\"
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"error": "La IA no devolvió un JSON válido. Por favor intenta de nuevo."}



def analizar_mensaje(user_id, mensaje):
    session = get_session(user_id)

    if session["fase"] == "esperando_datos":
        datos_extraidos = extraer_datos_ia(mensaje)
        if "error" in datos_extraidos:
            return datos_extraidos["error"]

        es_valido, resultado = procesar_datos(datos_extraidos)
        if not es_valido:
            return f"{resultado} Por favor corrige la información."

        session["datos"] = resultado
        session["fase"] = "esperando_confirmacion"

        resumen = (
            f"He entendido los siguientes datos:\n"
            f"- Nombre: {resultado['nombre']}\n"
            f"- Cédula: {resultado['cedula']}\n"
            f"- Tipo de contrato: {resultado['tipo_contrato']}\n\n"
            f"¿Confirmas que deseas generar el contrato con esta información?"
        )
        return resumen

    elif session["fase"] == "esperando_confirmacion":
        if mensaje.lower() in ["sí", "si", "perfecto", "de una", "dale", "avancemos"]:
            datos_finales = session["datos"]
            reset_session(user_id)
            return f"Contrato generado con éxito para {datos_finales['nombre']}. (Aquí iría la llamada al backend)"

        else:
            reset_session(user_id)
            return "Proceso cancelado. Si deseas iniciar de nuevo, proporciona los datos."
