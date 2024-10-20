from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, List

from clients.http import HttpClient
from .base import BackendBase


class Backend(BackendBase):
    def __init__(self, base_url: str, api_key=None, verify_ssl=True, timeout=10):
        super(Backend, self).__init__()
        self.client = HttpClient(base_url, api_key, verify_ssl, timeout)

    def list_available_models(self) -> Optional[list]:
        try:
            response = self.client.get("/v1/models")
            if not response:
                return None
            return response.json().get("data", [])
        except RequestException as e:
            print(f"Error retrieving list of models: {e}")
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
                "/v1/chat/completions",
                json=payload,
            )
            if not response:
                return None

            # Extract and return the generated text from the response
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["text"].strip()
            else:
                print("No valid response received from the model.")
                return None

        except RequestException as e:
            print(f"Error during the request to LocalAI: {e}")
            return None

    def embedding(self, text: str, model_name: str) -> Optional[List[float]]:
        payload = {"model": model_name, "input": text}

        try:
            response = self.client.post(
                "/embeddings",
                json=payload,
            )
            if not response:
                return None
            response.raise_for_status()

            result = response.json()
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            else:
                print("No valid embedding received from the model.")
                return None

        except RequestException as e:
            print(f"Error during the request to LocalAI for embedding: {e}")
            return None


# Example usage:
if __name__ == "__main__":
    backend = Backend(base_url="http://localhost:58080")

    # Example 1: Generating text
    prompt = "Tell me a story about a brave knight."
    generated_text = backend.generate(
        prompt, max_tokens=100, temperature=0.7, model_name="text-embedding-ada-002"
    )
    if generated_text:
        print(f"Generated Text: {generated_text}")

    # Example 3: List available models
    models = backend.list_available_models()
    if models:
        print(f"Available Models: {models}")

    # Example 4: Get embeddings for input text
    input_text = "Artificial intelligence is transforming industries."
    embedding = backend.embedding(input_text, "text-embedding-ada-002")
    if embedding:
        print(f"Embedding: {embedding}")
