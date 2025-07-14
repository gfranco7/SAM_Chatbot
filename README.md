# SAM_Chatbot


# Generador de Contratos Inteligente

Este proyecto implementa un agente conversacional que recopila datos clave (nombre, cédula, tipo de contrato) para generar contratos automáticamente. El sistema valida la información y la envía al backend para su procesamiento.

---

## 🧠 Funcionalidad Principal

- Extrae datos del mensaje del usuario usando una IA generativa (`gemini-1.5-flash`)
- Valida los datos extraídos: nombre, cédula (10 dígitos), tipo de contrato
- Solicita confirmación del usuario antes de enviar al backend
- Soporta los siguientes tipos de contrato:
  - **fijo**
  - **indefinido**
  - **prestación de servicios**

---

## 📁 Estructura del Proyecto

- `agent_logic.py` – Lógica principal del agente: análisis, validación y flujo conversacional.
- `session_store.py` – Manejo de sesiones para cada usuario.
- `config_qdrant.py` – Configuración del vector store (Qdrant) para RAG si se desea expandir.
- `qdrant_collection.py`, `retriever.py`, `ingest_pdf.py` – Utilidades para ingestar y recuperar información de PDFs (modo RAG).
- `chat_test.py`, `main.py` – Entradas para pruebas o ejecución directa del agente.
- `models.py` – Modelos de datos utilizados en la aplicación.
- `test.json` – Datos de ejemplo o pruebas.
- `requirements.txt` – Dependencias necesarias.
- `PDFs/` – Carpeta que contiene documentos PDF de referencia.
- `config/`, `__pycache__/`, `.env`, `.gitignore` – Archivos y carpetas de configuración y entorno.

---

## ⚙️ Requisitos

- Python 3.10+
- `google-generativeai`
- `python-dotenv`
- `qdrant-client`
- `fastapi` (si se conecta a backend)
- `uvicorn`
- `pydantic`
- `requests`

Instalación recomendada:

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

Ejecutar el agente conversacional desde `main.py` o `chat_test.py`:

```bash
python main.py
```

El sistema pedirá al usuario que proporcione su información en lenguaje natural. Luego:

1. Se extraen y validan los datos.
2. Se solicita confirmación.
3. Si el usuario acepta, los datos se envían al backend.

---

## 💡 Ejemplo

**Usuario escribe:**

```
Hola, soy Andrés García con cédula 1234567890. Quiero un contrato de prestación de servicios.
```

**Respuesta del sistema:**

```
Confirmación de datos:
- Nombre: Andrés García
- Cédula: 1234567890
- Tipo de contrato: prestacion

¿Deseas continuar con esta información?
```

---

## ✍️ Autor

**Gean Franco Jacome Laguna**

---

## 📜 Licencia

Este proyecto es para fines educativos. No se ha especificado una licencia de distribución.
