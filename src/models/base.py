from datetime import datetime

from db import db


def soft_deletable(cls):
    # Directly assign `deleted_at` column
    cls.deleted_at = db.Column(db.DateTime, nullable=True)

    # Define and assign the `soft_delete` method
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    cls.soft_delete = soft_delete

    # Define and assign the `query_active` class method
    @classmethod
    def query_active(cls):
        return cls.query.filter(cls.deleted_at.is_(None))

    cls.query_active = query_active

    return cls


def timestamped(cls):
    # Add `created_at` column directly
    cls.created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Add `updated_at` column directly
    cls.updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    return cls
