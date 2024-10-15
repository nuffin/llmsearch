import openai
from typing import Optional, List


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        """
        Initializes the OpenAI client with the specified API key and model.

        Args:
            api_key (str): Your OpenAI API key.
            model (str): The name of the model to be used for inference and embeddings.
        """
        openai.api_key = api_key
        self.model = model

    def generate(
        self,
        prompt: str,
        model: str,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        """
        Sends a request to OpenAI's API to generate text based on the input prompt.

        Args:
            prompt (str): The prompt or question to send to the OpenAI model.
            max_tokens (int, optional): The maximum number of tokens to generate. Default is 150.
            temperature (float, optional): The sampling temperature to control the randomness of output. Default is 1.0.

        Returns:
            str: The generated text or None if the request fails.
        """
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return (
                response.choices[0].text.strip()
                if response and len(response.choices) > 0
                else None
            )
        except Exception as e:
            print(f"Error during the request to OpenAI: {e}")
            return None

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Sends a request to OpenAI's API to generate embeddings from the input text.

        Args:
            text (str): The input text for which to generate embeddings.

        Returns:
            list: A list of floats representing the embedding vector, or None if the request fails.
        """
        try:
            response = openai.Embedding.create(model=self.model, input=text)
            return (
                response.data[0]["embedding"]
                if response and "data" in response and len(response.data) > 0
                else None
            )
        except Exception as e:
            print(f"Error during the request to OpenAI for embedding: {e}")
            return None

    def update_model(self, new_model: str) -> None:
        """
        Updates the current model used by the client.

        Args:
            new_model (str): The new model to be used for inference and embedding.
        """
        self.model = new_model
        print(f"Updated model to: {self.model}")


# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = OpenAIClient(api_key="your-api-key", model="text-davinci-003")

    # Example 1: Generating text
    prompt = "Explain the theory of relativity."
    generated_text = client.generate(prompt, max_tokens=100, temperature=0.7)
    if generated_text:
        print(f"Generated Text: {generated_text}")

    # Example 2: Get embeddings for input text
    input_text = (
        "Quantum mechanics and general relativity are fundamental theories in physics."
    )
    embedding = client.get_embedding(input_text)
    if embedding:
        print(f"Embedding: {embedding}")

    # Example 3: Update the model used by the client
    client.update_model("text-embedding-ada-002")
