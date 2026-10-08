import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_MODEL = "openai/gpt-oss-120b"


def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing from the .env file."
        )

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0,
        max_tokens=1200,
        max_retries=2,
        timeout=60,
    )