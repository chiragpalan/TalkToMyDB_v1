# app/vectorstore_client.py
from chromadb.utils import embedding_functions
import chromadb
from pathlib import Path
from .config import VECTORS_DIR

EMBED_FN = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_chroma_collection(collection_name="sakila_docs", persist_directory=None):
    persist_directory = persist_directory or str(VECTORS_DIR)
    Path(persist_directory).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist_directory))
    coll = client.get_or_create_collection(name=collection_name, embedding_function=EMBED_FN)
    return coll

def retrieve_context(query, k=5, collection_name="sakila_docs"):
    coll = get_chroma_collection(collection_name)
    res = coll.query(query_texts=[query], n_results=k)
    # res["documents"] is a list-of-lists: first item is list of docs
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return docs, metas
