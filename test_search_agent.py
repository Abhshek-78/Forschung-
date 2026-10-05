from langchain_ollama import ChatOllama


def main():

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    topic = (
        "Large Language Models "
        "in Healthcare"
    )

    prompt = f"""
You are an academic research assistant.

Research topic:
{topic}

Explain what kinds of academic papers
should be searched for this topic.

Give:
1. Important research areas
2. Important keywords
3. Important research questions
"""

    response = llm.invoke(
        prompt
    )

    print("\n")
    print("=" * 70)
    print("OLLAMA RESEARCH PLANNING")
    print("=" * 70)

    print(
        response.content
    )


if __name__ == "__main__":
    main()