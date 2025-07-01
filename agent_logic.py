import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import os
from session_store import *

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# models = genai.list_models()
# for m in models:
#     print(m.name, "-", m.supported_generation_methods)


model = genai.GenerativeModel("gemini-1.5-flash") 
confirmaciones = ["sí", "si", "perfecto", "dale", "de una", "ok", "avancemos", "yes"]

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
        "prestacion": ["servicios", "freelance", "prestacion de servicios", "prestaciones", "prestación"]
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

def analizar_mensaje(user_id, mensaje):
    session = get_session(user_id)

    if session["fase"] == "esperando_datos":
        datos_extraidos = extraer_datos_ia(mensaje)
        print("IA respondió:", datos_extraidos)

        if "error" in datos_extraidos:
            return f"{datos_extraidos['error']}"

        es_valido, resultado = procesar_datos(datos_extraidos)
        if not es_valido:
            return resultado

        session["datos"] = resultado
        session["fase"] = "esperando_confirmacion"

        resumen = (
            f"Confirmación de datos:\n"
            f"- Nombre: {resultado['nombre']}\n"
            f"- Cédula: {resultado['cedula']}\n"
            f"- Tipo de contrato: {resultado['tipo_contrato']}\n\n"
            f"¿Deseas continuar con esta información?"
        )
        return resumen

    elif session["fase"] == "esperando_confirmacion":
        if mensaje.lower().strip() in confirmaciones:
            datos_finales = session["datos"]
            reset_session(user_id)
            return f"¡Contrato generado para {datos_finales['nombre']}! Enviando datos al backend..."
        else:
            reset_session(user_id)
            return "Proceso cancelado. Puedes iniciar de nuevo cuando quieras."

def extraer_datos_ia(mensaje):
    prompt = f"""
Extrae del siguiente texto el nombre, la cédula (10 dígitos) y 
el tipo de contrato (fijo, indefinido, prestación). 
Corrige errores leves. Responde solo en formato JSON.

Si falta algún dato, responde con:
{{ "error": "falta el campo X" }}

Texto:
\"\"\"{mensaje}\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            return {"error": "La IA no devolvió un JSON válido"}

        json_text = match.group()
        return json.loads(json_text)

    except Exception as e:
        return {"error": f"No se pudo interpretar la respuesta de la IA: {e}"}
