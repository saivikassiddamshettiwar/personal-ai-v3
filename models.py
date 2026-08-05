import ollama


def get_available_providers():
    return [
        "Ollama",
        "OpenAI",
        "Gemini",
        "Claude"
    ]


def get_ollama_models():
    try:
        response = ollama.list()

        models = []

        for model in response["models"]:
            name = model["model"]

            # Hide embedding models
            if "embed" in name:
                continue

            models.append(name)

        return models

    except Exception:
        return ["llama3.2:3b"]


def get_openai_models():
    return [
        "gpt-5.5",
        "gpt-5-mini"
    ]


def get_gemini_models():
    return [
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    ]


def get_claude_models():
    return [
        "claude-opus-4",
        "claude-sonnet-4"
    ]


def get_models(provider):
    if provider == "Ollama":
        return get_ollama_models()

    elif provider == "OpenAI":
        return get_openai_models()

    elif provider == "Gemini":
        return get_gemini_models()

    elif provider == "Claude":
        return get_claude_models()

    return ["llama3.2:3b"]