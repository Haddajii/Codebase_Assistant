from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="llama3")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful coding assistant.
Answer the question using ONLY the context below and try to think based on the context provided .
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
)
