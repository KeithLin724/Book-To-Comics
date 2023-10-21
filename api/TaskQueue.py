# from collections import deque
from stable_diffusion import TextToImage
import os
from multiprocessing import Queue

FOLDER_PATH = "./image"


class TaskQueue:
    def __init__(self) -> None:
        self.task_queue: Queue = Queue()
        self.task_dict = {}

    def init(self):
        self.model = TextToImage()
        self.model.load()

        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)

        return

    def push_task(self, name: str, prompt: str) -> None:
        # self.task_queue.append((name, prompt))
        self.task_queue.put((name, prompt))
        self.task_state_map[frozenset((name, prompt))] = "waiting"
        return

    @staticmethod
    def handle_user_folder(user_name: str) -> str:
        path = os.path.join(FOLDER_PATH, user_name)
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def file_state(self, user_name: str, prompt: str) -> str:
        message = self.task_state_map.get(frozenset((user_name, prompt)), "Not find")

        if message == "Not find":
            check_file_path = os.path.join(FOLDER_PATH, user_name, f"{prompt}.jpg")
            return "finish" if os.path.exists(check_file_path) else "No this request"

        return message

    def run_generate_task_queue(self) -> None:
        # main run function
        print("open task queue")
        while True:
            if not self.task_queue.empty():
                task_name, task_prompt = self.task_queue.get()

                self.task_state_map[frozenset((task_name, task_prompt))] = "process"

                image = self.model.generate(prompt=task_prompt)

                user_save_folder_path = TaskQueue.handle_user_folder(
                    user_name=task_name,
                )

                file_path = os.path.join(user_save_folder_path, f"{task_prompt}.jpg")

                image.save(file_path)

                self.task_state_map[frozenset((task_name, task_prompt))] = "finish"
