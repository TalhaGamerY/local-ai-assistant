import requests
from config import OLLAMA_URL, TEXT_MODEL


class OllamaLLM:
    def __init__(self, model: str = TEXT_MODEL):
        self.model = model

    def generate(self, prompt: str, system: str = "", model: str | None = None) -> str:
        payload = {
            "model": model or self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return (
                "I cannot connect to Ollama. Make sure Ollama is running and the model is installed."
            )
        except Exception as error:
            return f"LLM error: {error}"
