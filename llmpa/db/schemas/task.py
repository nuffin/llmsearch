import uuid

from agents.task import TaskStatus
from ..postgres import db
from .base import timestamped, soft_deletable


@soft_deletable
@timestamped
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    status = db.Column(db.String, nullable=False, default=TaskStatus.PENDING)
    type = db.Column(db.String, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Task id={self.id}, type={self.type}>"
