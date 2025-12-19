from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="llama3")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful coding assistant.

RULES:
- Answer using ONLY the Context below. If not found, say: "I don't know based on the provided repo context."
- Output MUST be valid Markdown.
- Prefer a structured format with headings and lists.

FORMAT:
## Answer
(1-3 paragraphs max)

## Steps (if applicable)
1. ...
2. ...

## Code (if applicable)
Use fenced code blocks with a language tag, for example:
```js
// code here
```

## Notes (optional)
- ...

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
