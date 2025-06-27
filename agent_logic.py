import re
import os
import openai
import json

def extraer_datos_IA(texto_usuario):
    promt = f""" 
Extrae los siguientes campos del siguiente texto de manera estructurada en formato JSON:
- nombre (solo letras)
- num_id (solo números)
- tipo_contrato (entre fijo, indefinido o prestación)
Texto del usuario:
\"\"\"{texto_usuario}\"\"\"

Ejemplo de respuesta:
{{
    "nombre": "Juan Pérez", 
    "num_id": "1234567890",
    "tipo_contrato": "fijo"
}}

"""

    response = openai.ChatCompletion.create(
        model = "mistralai/mistral-7b-instruct", # Otra opcion 'openchat/openchat-7b'
        messages = [{"role":"user", "content": promt}],
        temperature = 0.2
    )
    content =response.choices[0].mesage.content

    try: 
        datos_extraidos = json.loads(content)
        return datos_extraidos
    except Exception as e:
        raise ValueError("La IA no devolvió un JSON válido. Error: " + str(e))




def procesar_datos(datos):

    nombre = datos.nombre.strip().title()
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        raise ValueError("El nombre solo puede contener letras y espacios")

    num_id = datos.num_id.strip()
    if not num_id.isdigit():
        raise ValueError("La identificación debe contener únicamente números, sin espacios ni símbolos")
    if len(num_id) != 10:
        raise ValueError("La identificación debe tener 10 dígitos")
    
    tipo_usuario = datos.tipo_contrato.strip().lower()
    tipos_validos = {
        "fijo": ["fijo", "temporal", "plazo", "a termino fijo", "término fijo"],
        "indefinido": ["indefinido", "a termino indefinido", "término indefinido", "sin plazo", "permanente"],
        "prestacion": ["prestación", "servicios", "prestacion de servicios", "freelance", "independiente"]
    }

    tipo_contrato_estandar = None
    for clave, sinonimos in tipos_validos.items():
        if tipo_usuario in sinonimos:
            tipo_contrato_estandar = clave
            break
    if not tipo_contrato_estandar:
        raise ValueError("El tipo de contrato no es válido o no es reconocido")

    return {
        "nombre": nombre,
        "num_id": num_id,
        "tipo_contrato": tipo_contrato_estandar
    }
