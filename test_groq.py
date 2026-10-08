from llm.groq_model import get_ollama_llm


def main():
    print("=" * 70)
    print("GROQCLOUD CONNECTION TEST")
    print("=" * 70)

    print("\nConnecting to GroqCloud...")

    llm = get_ollama_llm()

    response = llm.invoke(
        """
        You are an academic research assistant.

        Explain how Natural Language Processing can be used
        to translate spoken language during a video conference.

        Give three concise technical points.
        """
    )

    print("\nGroq response:")
    print("-" * 70)
    print(response.content)
    print("-" * 70)

    print("\nGroqCloud connection successful!")


if __name__ == "__main__":
    main()