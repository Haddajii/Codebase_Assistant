from loaders.repo_loader import clone_repo, load_repo_files, split_code_docs
from embeddings.vector_store import get_vector_store
from utils.retriever_utils import retrieve_docs
from llm.llm_chain import answer_from_docs

if __name__ == "__main__":
    repo_url = input("GitHub repo URL: ")
    question = input("Your question: ")

    repo_path, repo_id = clone_repo(repo_url)

    docs = load_repo_files(repo_path)
    splits = split_code_docs(docs)

    vector_store = get_vector_store(splits, repo_id)
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    retrieved_docs = retrieve_docs(question, retriever)
    answer = answer_from_docs(retrieved_docs, question)

    print("\nAnswer:\n", answer)
