class FileInfo:
    def __init__(
        self,
        fileId: str,
        name: str,
        path: str,
        originName: str,
        size: int,
        type: str,
        mimetype: str,
    ):
        self.name = name
        self.path = path
        self.originName = originName
        self.size = size
        self.type = type
        self.mimetype = mimetype

    def __repr__(self):
        return f"<FileInfo {self.name} ({self.type})>"
