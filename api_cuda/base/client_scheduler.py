from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx


class MonitorServer:
    def __init__(self, server_url: str, send_to_server_json: dict) -> None:
        self._scheduler = AsyncIOScheduler()
        self._server_url = server_url
        self._send_to_server_json = send_to_server_json
        self._check: bool = False

    def start(self) -> None:
        self._scheduler.start()
        self.start_connect_server()
        return

    def close(self, need_wait_job: bool = True) -> None:
        self._scheduler.remove_all_jobs()
        self._scheduler.shutdown(wait=need_wait_job)
        return

    def start_connect_server(self, second: int):
        self._scheduler.add_job(
            self._connect_server,
            "interval",
            seconds=second,
            id="connect_server",
        )

    async def _connect_server(self) -> None:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    self._server_url,
                    json=self._send_to_server_json,
                )
            # if success connect
            if res.status_code == 200:
                self._scheduler.remove_job("connect_server")
                self.check_server_is_alive()

        except Exception as e:
            print(f"error: {str(e)} , server service is close")

    def check_server_is_alive(self):
        self._scheduler.add_job(
            self._check_server_alive,
            "interval",
            second=10,
            id="check_server_connect",
        )

    async def _check_server_alive(self):
        if self._check == True:
            self._check = False
            return

        # else
        self._scheduler.remove_job("check_server_connect")
        self.start_connect_server()

        return

    def server_check_point(self, server_check: bool):
        self._check = server_check
