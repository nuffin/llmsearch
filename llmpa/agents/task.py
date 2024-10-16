from enum import Enum


class TaskType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

    COMPUTE = "compute"
    CODING = "coding"
    WRITING = "writing"
    CONVERTING = "converting"

    TEXT2SPEECH = "text2speech"
    SPEECH2TEXT = "speech2text"
    TEXT2IMAGE = "text2image"
    IMAGE2TEXT = "image2text"

    LEARNING = "learning"
    TRAINING = "training"
    SEARCHING = "searching"

    @classmethod
    def isValid(cls, task_type):
        return task_type in cls._value2member_map_


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"

    @classmethod
    def isValid(cls, status):
        return status in cls._value2member_map_


class Task:

    def __init__(self, task_type: TaskType):
        self.type = task_type
        self.status = TaskStatus.PENDING
        self.data = {}
