from .task import Task


class BaseAgent:

    def perform(self, task: Task):
        raise NotImplementedError
