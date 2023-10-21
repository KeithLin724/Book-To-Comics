from collections import deque


class TaskQueue:
    def __init__(self, model) -> None:
        self.model = model
        self.task_queue = deque()
        self.task_map = {}

    def push_task(self, name: str, prompt: str):
        self.task_queue.append((name, prompt))

        return
