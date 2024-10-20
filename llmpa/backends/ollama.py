import requests
from typing import List, Optional

from clients.http import HttpClient
from .base import BackendBase, JsonType


class Backend(BackendBase):
    def __init__(self, base_url: str, timeout: Optional[int] = 10):
        super(Backend, self).__init__()
        self.client = HttpClient(base_url, timeout)

    def get_model_info(self, model_name: str) -> Optional[JsonType]:
        payload = {"name": model_name}

        try:
            response = self.client.post("/api/show", json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving model info: {e}")
            return None

    def generate(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = self.client.post(
                "/api/generate",
                json=payload,
            )
            if not response:
                return None

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["text"].strip()
            else:
                print("No valid response received from the model.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error during the request to Ollama: {e}")
            return None

    def embedding(self, text: str, model_name: str) -> Optional[List[float]]:
        payload = {"model": model_name, "input": text}

        try:
            response = self.client.post(
                "/api/embeddings",
                headers=headers,
                json=payload,
            )
            if not response:
                return None

            result = response.json()
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            else:
                print("No valid embedding received from the model.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error during the request to Ollama for embedding: {e}")
            return None


# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = Backend(base_url="http://localhost:51400")

    # Example 1: Generating text
    prompt = "Describe the future of AI."
    generated_text = client.generate(prompt, max_tokens=100, temperature=0.7)
    if generated_text:
        print(f"Generated Text: {generated_text}")

    # Example 2: Get embeddings for input text
    input_text = "Machine learning is a subset of artificial intelligence."
    embedding = client.embedding(input_text)
    if embedding:
        print(f"Embedding: {embedding}")
