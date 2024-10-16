import requests
import json
from typing import Optional, List

from .base import ClientBase


class LocalAIClient(ClientBase):
    def __init__(self, base_url: str, timeout: Optional[int] = 10):
        """
        Initializes the LocalAI client with the specified server base URL.

        Args:
            base_url (str): The base URL of the LocalAI server (e.g., "http://localhost:8080").
            timeout (int, optional): Timeout for the HTTP requests. Default is 10 seconds.
        """
        super(LocalAIClient, self).__init__(base_url, timeout)

    def get_model_info(self, model: str) -> Optional[dict]:
        """
        Retrieves model information from the LocalAI server.

        Returns:
            dict: Model information as a dictionary, or None if the request fails.
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/models/{model}", timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving model information: {e}")
            return None

    def list_available_models(self) -> Optional[list]:
        """
        Retrieves a list of available models from the LocalAI server.

        Returns:
            list: List of available models, or None if the request fails.
        """
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving list of models: {e}")
            return None

    def generate(
        self,
        model: str,
        prompt: str,
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
            response = requests.post(
                f"{self.base_url}/v1/generate",
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout,
            )
            response.raise_for_status()

            # Extract and return the generated text from the response
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["text"].strip()
            else:
                print("No valid response received from the model.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error during the request to LocalAI: {e}")
            return None

    def embedding(self, model: str, text: str) -> Optional[List[float]]:
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
            print(f"Error during the request to LocalAI for embedding: {e}")
            return None


# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = LocalAIClient(base_url="http://localhost:8080")

    # Example 1: Generating text
    prompt = "Tell me a story about a brave knight."
    generated_text = client.generate(prompt, max_tokens=100, temperature=0.7)
    if generated_text:
        print(f"Generated Text: {generated_text}")

    # Example 2: Get model information
    model_info = client.get_model_info()
    if model_info:
        print(f"Model Information: {json.dumps(model_info, indent=2)}")

    # Example 3: List available models
    models = client.list_available_models()
    if models:
        print(f"Available Models: {models}")

    # Example 4: Get embeddings for input text
    input_text = "Artificial intelligence is transforming industries."
    embedding = client.embedding(input_text)
    if embedding:
        print(f"Embedding: {embedding}")

    # Example 5: Update the model used by the client
    client.update_model("another-model-name")
