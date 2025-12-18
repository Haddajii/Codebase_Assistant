from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

BATCH_SIZE = 256

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
        for i in range(0, len(documents), BATCH_SIZE):
            batch = documents[i:i + BATCH_SIZE]
            vector_store.add_documents(batch)
            print(f"Embedded {i + len(batch)} / {len(documents)} chunks")

    else:
        print("Using cached embeddings")

    return vector_store
