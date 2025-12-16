from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def get_vector_store(documents, repo_id):
    persist_dir = f"./chroma_langchain_db/{repo_id}"

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    vector_store = Chroma(
        collection_name=repo_id,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    if vector_store._collection.count() == 0:
        print("Building embeddings (first time)...")
        vector_store.add_documents(documents)
    else:
        print("Using cached embeddings")

    return vector_store
