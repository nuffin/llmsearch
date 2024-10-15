from typing import Optional, List


class ClientBase:
    def __init__(self, base_url: str, timeout: Optional[int] = 10):
        self.base_url = base_url
        self.timeout = timeout

    def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        raise NotImplementedError

    def embedding_text(self, model: str, text: str) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_image(self, model: str, filepath: str) -> Optional[List[float]]:
        raise NotImplementedError
