import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Any, Dict, List, Optional, Union


def insert_path():
    import os
    import sys

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


insert_path()
del insert_path

from schemas.file import FileInfo


JsonType = Dict[str, Any]


class BackendBase:
    def get_model_info(self, model_name: str) -> Optional[dict]:
        raise NotImplementedError

    def list_available_models(self) -> Optional[list]:
        raise NotImplementedError

    def generate(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        raise NotImplementedError

    def embedding(
        self,
        target: Optional[Union[str, FileInfo]] = None,
        model_name: Optional[str] = None,
    ) -> Optional[List[float]]:
        if isinstance(target, FileInfo):
            return self.embedding_file(target, model_name)
        elif isinstance(target, str):
            return self.embedding_text(target, model_name)
        else:
            raise ValueError("Either text or fileInfo must be provided")

    def embedding_file(
        self, fileInfo: FileInfo, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        if not fileInfo:
            return None
        if fileInfo.type == "text":
            content = open(fileInfo.path, "r").read()
            return self.embedding_text(content, model_name)
        elif fileInfo.type == "image":
            return self.embedding_image(fileInfo, model_name)
        elif fileInfo.type == "audio":
            return self.embedding_audio(fileInfo, model_name)
        elif fileInfo.type == "video":
            return self.embedding_video(fileInfo, model_name)
        else:
            """
            TODO: maybe complex multimedia files like docx, pptx, pdf, etc., should extract each part
            """
            raise ValueError(f"Unsupported file type: {fileInfo}")

    def embedding_text(
        self, text: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_image(
        self, filepath: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_audio(
        self, filepath: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_video(
        self, filepath: str, model_name: Optional[str] = None
    ) -> Optional[List[float]]:
        raise NotImplementedError
