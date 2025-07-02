import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid

#Configuraciòn del modelo y ruta pdf
PDF_PATH = "PDFs/instrucciones_IA.pdf"      
COLLECTION_NAME = "contrato_pdf_embeddings"     
EMBEDDING_MODEL = "all-MiniLM-L6-v2"            # Modelo eficiente (384 dim)



qdrant = QdrantClient("http://localhost:6333") #SE carga la coneccion a qdrant 
#TIene que estar corriendo el docker



model = SentenceTransformer(EMBEDDING_MODEL)



def extraer_texto(pdf_path):
    doc = fitz.open(pdf_path)
    texto_total = ""
    for page in doc:
        texto_total += page.get_text()
    return texto_total

def dividir_en_chunks(texto, max_len=250):
    oraciones = texto.split(".")
    chunks, actual = [], ""

    for o in oraciones:
        if len(actual) + len(o) < max_len:
            actual += o.strip() + ". "
        else:
            chunks.append(actual.strip())
            actual = o.strip() + ". "

    if actual:
        chunks.append(actual.strip())

    return chunks

def crear_embeddings(chunks):
    return model.encode(chunks).tolist()

def subir_a_qdrant(chunks, vectores):
    puntos = []
    for i, (texto, vector) in enumerate(zip(chunks, vectores)):
        puntos.append(models.PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"texto": texto}
        ))

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=puntos
    )


print("Leyendo PDF... \n")
texto = extraer_texto(PDF_PATH)
print("🔍 Texto extraído:\n", texto)

print("Dividiendo en fragmentos...\n")
chunks = dividir_en_chunks(texto)

print("Creando embeddings...\n")
vectores = crear_embeddings(chunks)

print("Subiendo a Qdrant...\n")
subir_a_qdrant(chunks, vectores)

print(f"¡Listo! Se subieron {len(chunks)} fragmentos a la colección '{COLLECTION_NAME}' en Qdrant.")
