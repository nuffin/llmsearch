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
    userId = db.Column(db.Integer, index=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    originName = db.Column(db.String, nullable=False)
    fileSize = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<File {self.name}>"
