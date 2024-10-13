from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

from db import db


class SoftDeletable(db.Model):
    __abstract__ = True

    @declared_attr
    def deleted_at(cls):
        return db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    @classmethod
    def query_active(cls):
        return cls.query.filter(cls.deleted_at.is_(None))


class Timestamped(db.Model):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
