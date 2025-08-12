import chromadb
from chromadb.utils import embedding_functions

EMBED_MODEL = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_or_create_collection():
    """Returns a persistent Chroma collection for schema/document storage."""
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_or_create_collection(name="schema_docs", embedding_function=EMBED_MODEL)

def add_documents(collection, docs):
    """Adds documents to the Chroma collection."""
    collection.add(
        ids=[d["id"] for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[d["metadata"] for d in docs]
    )
