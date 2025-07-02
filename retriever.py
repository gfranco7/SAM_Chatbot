from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest



COLLECTION_NAME = "contrato_pdf_embeddings"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3  # fragmentos relevantes a recuperar

qdrant = QdrantClient("http://localhost:6333")
model = SentenceTransformer(EMBEDDING_MODEL)



def obtener_contexto_relevante(mensaje_usuario, top_k=TOP_K):
    consulta_vector = model.encode(mensaje_usuario).tolist()

    resultados = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=consulta_vector,
        limit=top_k,
        with_payload=True)

    fragmentos = [r.payload["texto"] for r in resultados if "texto" in r.payload]
    return "\n\n".join(fragmentos)



if __name__ == "__main__":
    consulta = input("¿Qué desea saber el usuario?:\n> ")
    contexto = obtener_contexto_relevante(consulta)
    print("\nFragmentos más relevantes:\n")
    print(contexto)
