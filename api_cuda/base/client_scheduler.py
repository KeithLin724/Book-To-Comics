from apscheduler.schedulers.asyncio import AsyncIOScheduler


class MonitorServer:
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.start()
        return

    def close(self) -> None:
        self._scheduler.shutdown()
        return
