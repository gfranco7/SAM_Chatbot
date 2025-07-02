from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient("http://localhost:6333")


collection_name = "contrato_pdf_embeddings"


if collection_name in client.get_collections().collections:
    print(f"La colección '{collection_name}' ya existe.")
else:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384, 
            distance=Distance.COSINE,
        )
    )
    print(f"Colección '{collection_name}' creada correctamente.")
