from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx


class MonitorServer:
    def __init__(self, connect_server_url: str, send_to_server_json: dict) -> None:
        self._scheduler = AsyncIOScheduler()
        self._server_url = connect_server_url
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

    def start_connect_server(self, second: int = 5):
        """
        first or reconnect to server to use

        The `start_connect_server` function starts a scheduled task that connects to a server at a specified
        interval and checks if the connection is successful.

        Parameters
        ----------
        second : int
            The `second` parameter in the `start_connect_server` method represents the interval in seconds at
        which the `_connect_server` function will be executed. It determines how often the server connection
        will be attempted.

        """
        JOB_ID = "connect_server"

        async def _connect_server() -> None:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.post(
                        self._server_url,
                        json=self._send_to_server_json,
                    )
                # if success connect
                if res.status_code == 200:
                    self.check_server_is_alive()
                    self._scheduler.remove_job(JOB_ID)

            except Exception as e:
                print(f"error: {str(e)} , server:({self._server_url}) service is close")

        self._scheduler.add_job(
            _connect_server,
            "interval",
            seconds=second,
            id=JOB_ID,
        )

    def check_server_is_alive(self):
        """
        always running

        The function `check_server_is_alive` periodically checks if the server is alive and takes
        appropriate actions if it is not.

        """
        JOB_ID = "check_server_connect"

        async def _check_server_alive():
            if self._check == True:
                self._check = False
                return

            # else
            self.start_connect_server()
            self._scheduler.remove_job(JOB_ID)
            return

        self._scheduler.add_job(
            _check_server_alive,
            "interval",
            seconds=10,
            id=JOB_ID,
        )

    def server_check_point(self, server_check: bool):
        self._check = server_check
