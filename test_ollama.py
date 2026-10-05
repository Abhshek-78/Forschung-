from langchain_ollama import ChatOllama


def main():

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    response = llm.invoke(
        "Explain what an academic research paper is in two sentences."
    )

    print("\nOllama response:\n")
    print(response.content)


if __name__ == "__main__":
    main()