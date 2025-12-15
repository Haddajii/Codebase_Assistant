from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def get_vector_store(documents, collection_name="repo_collection", persist_dir="./chroma_langchain_db"):
    embeddings = OllamaEmbeddings(model="mxbai-embed-large") 
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    

    vector_store.add_documents(documents)
    
    return vector_store
