import requests
import json
from typing import Optional, List

from .base import ClientBase


class OllamaClient(ClientBase):
    def __init__(self, base_url: str, timeout: Optional[int] = 10):
        """
        Initializes the Ollama client with the specified server base URL.

        Args:
            base_url (str): The base URL of the Ollama server (e.g., "http://localhost:11434").
            timeout (int, optional): Timeout for the HTTP requests. Default is 10 seconds.
        """
        super(OllamaClient, self).__init__(base_url, timeout)

    def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        """
        Sends a request to the Ollama server to generate text based on the input prompt.

        Args:
            model (str): The name of the model to be used for inference and embeddings.
            prompt (str): The prompt or question to send to the Ollama model.
            max_tokens (int, optional): The maximum number of tokens to generate. Default is 150.
            temperature (float, optional): The sampling temperature to control the randomness of output. Default is 1.0.

        Returns:
            str: The generated text or None if the request fails.
        """
        headers = {"Content-Type": "application/json"}

        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                f"{self.base_url}/v1/generate",
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout,
            )
            response.raise_for_status()

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["text"].strip()
            else:
                print("No valid response received from the model.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error during the request to Ollama: {e}")
            return None

    def embedding(self, model: str, text: str) -> Optional[List[float]]:
        """
        Sends a request to the Ollama server to generate embeddings from the input text.

        Args:
            model (str): The name of the model to be used for inference and embeddings.
            text (str): The input text for which to generate embeddings.

        Returns:
            list: A list of floats representing the embedding vector, or None if the request fails.
        """
        headers = {"Content-Type": "application/json"}

        payload = {"model": model, "input": text}

        try:
            response = requests.post(
                f"{self.base_url}/v1/embeddings",
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout,
            )
            response.raise_for_status()

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
    client = OllamaClient(base_url="http://localhost:11434", model="your-model-name")

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

    # Example 3: Update the model used by the client
    client.update_model("another-model-name")
