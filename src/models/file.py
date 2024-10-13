from db import db
from .base import timestamped, soft_deletable


@soft_deletable
@timestamped
class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, index=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    originName = db.Column(db.String, nullable=False)
    fileSize = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<File {self.name}>"
