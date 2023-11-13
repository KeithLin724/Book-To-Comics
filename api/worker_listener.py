from base import REDIS_CONNECT, LOGGER
from rq import Worker, Connection
import asyncio


class WorkListener:
    def __init__(self, worker_list: list) -> None:
        self._work_list = worker_list

    async def _work_listener(self):
        try:
            with Connection(REDIS_CONNECT):
                worker = Worker(self._work_list)
                worker.work()
        except asyncio.CancelledError:
            LOGGER.info("Worker listener is cancel")

    def start(self):
        self._listen_task = asyncio.create_task(self._work_listener())
        LOGGER.info("Worker Listener is open")
        return

    def close(self):
        self._listen_task.cancel()
        LOGGER.info("Worker Listener is close")
        return
