import os
import openai

openai.api_key = os.getenv("OPENROUTER_API_KEY")  
openai.api_base = "https://openrouter.ai/api/v1"

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
  "salario": 3000000
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














"""
Estoy creando un chatbox el cual tiene la función de generar contratos. Contexto: estoy elaborando el agente, pero tengo que conectarlo con fronted y backend. Entonces mi cliente quiere poder interactuar con el agente, saludar, y escribir que tipo de contrato quiere generar """