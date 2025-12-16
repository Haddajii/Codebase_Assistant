from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

def get_vector_store(documents, repo_id):
    persist_dir = f"./chroma_langchain_db/{repo_id}"
    os.makedirs(persist_dir, exist_ok=True)

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    vector_store = Chroma(
        collection_name=repo_id,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    if len(vector_store.get()["ids"]) == 0:
        vector_store.add_documents(documents)

    return vector_store
