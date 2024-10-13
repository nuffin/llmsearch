import bcrypt
from sqlalchemy import event

from db import db
from .base import Timestamped, SoftDeletable


class User(Timestamped, SoftDeletable):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


def hash_password(mapper, connection, target):
    if target.password:
        target.password = bcrypt.hashpw(
            target.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")


# Listen for the 'before_insert' event
event.listen(User, "before_insert", hash_password)
event.listen(User, "before_update", hash_password)
