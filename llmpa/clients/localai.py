import json
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, List

from .base import ClientBase


class LocalAIClient(ClientBase):
    def __init__(self, base_url: str, api_key=None, verify_ssl=True, timeout=10):
        """
        Initializes the LocalAI client with the specified server base URL.

        Args:
            base_url (str): The base URL of the LocalAI server (e.g., "http://localhost:8080").
            timeout (int, optional): Timeout for the HTTP requests. Default is 10 seconds.
        """
        super(LocalAIClient, self).__init__(base_url, api_key, verify_ssl, timeout)

    def list_available_models(self) -> Optional[list]:
        """
        Retrieves a list of available models from the LocalAI server.

        Returns:
            list: List of available models, or None if the request fails.
        """
        try:
            response = self.get("/v1/models", timeout=self.timeout)
            print(response.json())
            if not response:
                return None
            response.raise_for_status()
            return response.json().get("data", [])
        except RequestException as e:
            print(f"Error retrieving list of models: {e}")
            return None

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        """
        Sends a request to the LocalAI server to generate text based on the input prompt.

        Args:
            model (str): The name of the model to be used for inference and embeddings.
            prompt (str): The prompt or question to send to the LocalAI model.
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
            response = self.post(
                "/v1/chat/completions",
                json=payload,
                timeout=self.timeout,
            )
            if not response:
                return None
            response.raise_for_status()

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

    def embedding(self, text: str, model: str) -> Optional[List[float]]:
        """
        Sends a request to the LocalAI server to generate embeddings from the input text.

        Args:
            model (str): The name of the model to be used for inference and embeddings.
            text (str): The input text for which to generate embeddings.

        Returns:
            list: A list of floats representing the embedding vector, or None if the request fails.
        """
        headers = {"Content-Type": "application/json"}

        payload = {"model": model, "input": text}

        try:
            response = self.post(
                "/embeddings",
                extra_headers=headers,
                json=payload,
                timeout=self.timeout,
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
    # Initialize the client
    client = LocalAIClient(base_url="http://localhost:58080")

    # Example 1: Generating text
    prompt = "Tell me a story about a brave knight."
    generated_text = client.generate(
        prompt, max_tokens=100, temperature=0.7, model="text-embedding-ada-002"
    )
    if generated_text:
        print(f"Generated Text: {generated_text}")

    # Example 3: List available models
    models = client.list_available_models()
    if models:
        print(f"Available Models: {models}")

    # Example 4: Get embeddings for input text
    input_text = "Artificial intelligence is transforming industries."
    embedding = client.embedding(input_text, "text-embedding-ada-002")
    if embedding:
        print(f"Embedding: {embedding}")

    # Example 5: Update the model used by the client
    # client.update_model("another-model-name")
