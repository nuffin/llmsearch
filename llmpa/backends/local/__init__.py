from typing import Optional, List

from ..base import BackendBase
from .models import efficientnet
from .models import resnet
from .models import x3d


class LocalBackend(BackendBase):
    def __init__(self, timeout: Optional[int] = 10):
        """
        Initializes the Local client.

        Args:
            timeout (int, optional): Timeout for the HTTP requests. Default is 10 seconds.
        """
        super(LocalBackend, self).__init__(None, timeout)

    def embedding_text(self, model: str, text: str) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_image(self, model: str, filepath: str) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_video(self, model: str, filepath: str) -> Optional[List[float]]:
        raise NotImplementedError
