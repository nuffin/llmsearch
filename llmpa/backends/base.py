import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, List


class BackendBase:
    def get_model_info(self, model: str) -> Optional[dict]:
        raise NotImplementedError

    def list_available_models(self) -> Optional[list]:
        raise NotImplementedError

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        raise NotImplementedError

    def embedding(
        self, model: str, text: Optional[str] = None, filepath: Optional[str] = None
    ) -> Optional[List[float]]:
        if filepath:
            return self.embedding_file(model, filepath)
        elif text:
            return self.embedding_text(model, text)

    def embedding_text(self, model: str, text: str) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_file(self, model: str, filepath: str) -> Optional[List[float]]:
        raise NotImplementedError
