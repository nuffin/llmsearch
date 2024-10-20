from typing import Optional, List

from ..base import BackendBase
from .models import image
from .models import video


class LocalBackend(BackendBase):
    def __init__(self):
        super(LocalBackend, self).__init__()

    def embedding_text(
        self, text: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_image(
        self, filepath: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        extractor = image.EmbeddingExtractor(model_name=model_name)

    def embedding_audio(
        self, filepath: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_video(
        self, filepath: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError
