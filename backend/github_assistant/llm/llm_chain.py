from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="llama3")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful coding assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
)

def answer_from_docs(docs, question: str):
    sources = sorted(set(
        doc.metadata.get("source", "unknown")
        for doc in docs
    ))

    context = "\n\n".join(
        f"File: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )


    final_prompt = prompt.format(
        context=context,
        question=question
    )

    answer =  llm.invoke(final_prompt)
    return answer , sources 
