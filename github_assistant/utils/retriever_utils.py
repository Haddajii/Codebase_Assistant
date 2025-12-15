def ask(question: str, retriever, llm, prompt):
    docs = retriever.invoke(question)
    if not docs:
        print("No documents retrieved for this question")
        context = "No context available"
    else:
        context = "\n\n".join(doc.page_content for doc in docs)


    final_prompt = prompt.format(
        context=context,
        question=question
    )

    return llm.invoke(final_prompt)
