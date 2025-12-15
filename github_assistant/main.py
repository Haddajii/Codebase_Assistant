from loaders.repo_loader import clone_repo, load_repo_files, split_code_docs
from embeddings.vector_store import get_vector_store
from llm.llm_chain import llm, prompt
from utils.retriever_utils import ask

repo_url = ""
repo_dir = clone_repo(repo_url)

docs = load_repo_files(repo_dir)
all_splits = split_code_docs(docs)


vector_store = get_vector_store(all_splits)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 20})



questions = [
    "where and how is the login implemeted "
]

for q in questions:

    answer = ask(q, retriever, llm, prompt)
    print(f"Q: {q}\nA: {answer}\n{'-'*40}")
