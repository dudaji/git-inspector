from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(**kwargs):
    return ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", **kwargs)
