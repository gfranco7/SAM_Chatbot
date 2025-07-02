from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "contrato_pdf_embeddings"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


qdrant = QdrantClient("http://localhost:6333")

model = SentenceTransformer(EMBEDDING_MODEL)
