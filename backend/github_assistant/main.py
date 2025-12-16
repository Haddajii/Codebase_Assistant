from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loaders.repo_loader import clone_repo, load_repo_files, split_code_docs
from embeddings.vector_store import get_vector_store
from llm.llm_chain import answer_from_docs
from utils.retriever_utils import retrieve_docs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_cache = {}

class LoadRepoRequest(BaseModel):
    repo_url: str

class AskRequest(BaseModel):
    repo_id: str
    question: str

@app.post("/load_repo")
def load_repo_endpoint(req: LoadRepoRequest):
    repo_path, repo_id = clone_repo(req.repo_url)
    docs = load_repo_files(repo_path)
    all_splits = split_code_docs(docs)

    if repo_id in vector_cache:
        vector_store = vector_cache[repo_id]
        msg = "Using cached embeddings"
    else:
        vector_store = get_vector_store(all_splits, repo_id)
        vector_cache[repo_id] = vector_store
        msg = "Created new embeddings"

    return {
        "repo_id": repo_id,
        "num_files": len(docs),
        "num_chunks": len(all_splits),
        "message": msg
    }

@app.post("/ask")
def ask_question(req: AskRequest):
    vector_store = vector_cache.get(req.repo_id)
    if not vector_store:
        return {"error": "Repo not loaded"}

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    docs = retrieve_docs(req.question, retriever)
    answer, sources = answer_from_docs(docs, req.question)

    sources = [ "\\".join(src.split("\\")[2:]) for src in sources ]
    return {"answer": answer, "sources": sources}
