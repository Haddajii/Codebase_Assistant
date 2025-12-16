import os
import stat
import hashlib
from git import Repo
from langchain_core.documents import Document

# ---------- Utils ----------

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def repo_id_from_url(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

# ---------- Repo cloning ----------

def clone_repo(repo_url: str, base_dir="data"):
    repo_id = repo_id_from_url(repo_url)
    repo_path = os.path.join(base_dir, repo_id)

    if not os.path.exists(repo_path):
        print(f"Cloning {repo_url} → {repo_path}")
        Repo.clone_from(repo_url, repo_path)

    return repo_path, repo_id

# ---------- Load files ----------

def load_repo_files(repo_dir):
    docs = []

    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".java"):  # keep it strict for now
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        docs.append(
                            Document(
                                page_content=content,
                                metadata={"source": path}
                            )
                        )
                except Exception as e:
                    print(f"❌ Failed to read {path}: {e}")

    print(f"Loaded {len(docs)} source files")
    return docs

# ---------- Split ----------

def split_code_docs(docs, chunk_size=1000):
    all_splits = []

    for doc in docs:
        lines = doc.page_content.splitlines()
        chunk = []

        for line in lines:
            chunk.append(line)
            if len("\n".join(chunk)) >= chunk_size:
                all_splits.append(
                    Document(
                        page_content="\n".join(chunk),
                        metadata=doc.metadata
                    )
                )
                chunk = []

        if chunk:
            all_splits.append(
                Document(
                    page_content="\n".join(chunk),
                    metadata=doc.metadata
                )
            )

    print(f"Created {len(all_splits)} chunks")
    return all_splits
