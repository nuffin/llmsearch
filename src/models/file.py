from db import db
from .base import Timestamped, SoftDeletable


class File(Timestamped, SoftDeletable):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<File {self.name}>"
