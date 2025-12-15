import os
import shutil
import stat
import hashlib
from git import Repo
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def repo_id_from_url(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def clone_repo(repo_url: str, repo_dir="data/repo_tmp"):
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir, onerror=remove_readonly)

    print(f"Cloning {repo_url} into {repo_dir}...")
    Repo.clone_from(repo_url, repo_dir)
    return repo_dir

def load_repo_files(repo_dir):
    docs = []
    for root, _, files in os.walk(repo_dir):
        for f in files:
            if f.endswith(".java"):  
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as file:
                    content = file.read()
                    docs.append(Document(page_content=content, metadata={"source": path}))
    return docs

def split_code_docs(docs, chunk_size=1000):
    all_splits = []
    for doc in docs:
        code = doc.page_content
        lines = code.splitlines()
        chunk = []
        for line in lines:
            chunk.append(line)
            if len("\n".join(chunk)) > chunk_size:
                all_splits.append(Document(
                    page_content="\n".join(chunk),
                    metadata={"source": doc.metadata['source']}
                ))
                chunk = []
        if chunk:
            all_splits.append(Document(
                page_content="\n".join(chunk),
                metadata={"source": doc.metadata['source']}
            ))
    return all_splits
