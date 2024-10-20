import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .base import timestamped, soft_deletable


@soft_deletable
@timestamped
class File(db.Model):
    __tablename__ = "files"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    userId = db.Column(db.String, index=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    originName = db.Column(db.String, nullable=False)
    fileSize = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<File {self.name}>"


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
        return f"<FileInfo {self.name} ({self.fileType})>"
