import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, List


class BaseBackend:
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

    def embedding_text(self, text: str, model: str) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_file(self, filepath: str, model: str) -> Optional[List[float]]:
        raise NotImplementedError
