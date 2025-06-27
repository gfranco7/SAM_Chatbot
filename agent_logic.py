from fastapi import FastAPI, HTTPException
import re
import os
import openai



openai.api_key = os.getenv("OPENROUTER_API_KEY")  
openai.api_base = "https://openrouter.ai/api/v1"
app = FastAPI()

def extraer_datos_con_ia(texto_usuario):
    prompt = f"""
Extrae los siguientes campos del siguiente texto de manera estructurada en formato JSON:
- nombre (solo letras)
- cedula (solo números)
- tipo_contrato (entre fijo, indefinido o prestacion)
- salario (solo número en pesos)

Texto del usuario:
\"\"\"{texto_usuario}\"\"\"

Ejemplo de respuesta:
{{
  "nombre": "Juan Pérez",
  "cedula": "123456789",
  "tipo_contrato": "fijo",
}}
"""

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",  
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        datos_extraidos = eval(content) 
        return datos_extraidos
    except Exception as e:
        raise ValueError("La IA no devolvió un JSON válido. Error: " + str(e))



def procesar_datos(datos):
    """
    Valida y limpia los datos extraídos (sea por formulario o IA).
    Devuelve un dict listo para el backend.
    """

    nombre = datos.nombre.strip().title()
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        raise ValueError("El nombre solo puede contener letras y espacios")

    cedula = datos.cedula.strip()
    if not cedula.isdigit():
        raise ValueError("La cédula debe contener solo números")

    tipo_usuario = datos.tipo_contrato.strip().lower()

    tipos_validos = {
        "fijo": ["fijo", "temporal", "plazo", "a termino fijo", "término fijo"],
        "indefinido": ["indefinido", "a termino indefinido", "término indefinido", "permanente"],
        "prestacion": ["prestacion", "servicios", "freelance", "prestación de servicios"]
    }

    tipo_contrato_estandar = None
    for clave, sinonimos in tipos_validos.items():
        if tipo_usuario in sinonimos:
            tipo_contrato_estandar = clave
            break

    if not tipo_contrato_estandar:
        raise ValueError("El tipo de contrato no es reconocido")

    return {
        "nombre": nombre,
        "cedula": cedula,
        "tipo_contrato": tipo_contrato_estandar,
    }



