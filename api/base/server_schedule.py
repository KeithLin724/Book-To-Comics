from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from apscheduler.events import EVENT_JOB_ERROR

from . import LOGGER
import httpx


class MonitorMicroServer:
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()
        self._micro_service_dict = {}
        # add job event to remove the connect
        # self._scheduler.add_listener(
        #     self._job_exception,
        #     EVENT_JOB_ERROR,
        # )

    def start(self):
        self._scheduler.start()

    # def _job_exception(self, event):
    #     if event.exception:
    #         # LOGGER.warning(f"error({event.job_id}): {str(event.exception)}")
    #         print(f"error({event.job_id}): {str(event.exception)}")
    #         # self._scheduler.remove_job(event.job_id)
    #         job = self._scheduler.get_job(event.job_id)
    #         if job:
    #             self._scheduler.remove_job(event.job_id)

    def _make_monitor(self, url: str, task_id: str):
        async def get_alive() -> None:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(url)
                    print(res.status_code)
            except Exception as e:
                LOGGER.warning(f"error({task_id}): {str(e)} , micro service is close")
                self._micro_service_dict.pop(task_id)
                self._scheduler.remove_job(task_id)

        return get_alive

    # first is the type , second is the url
    def add_micro_server(
        self,
        micro_server_name: str,
        micro_server_url: str,
        second: int = 5,
    ) -> None:
        # add job
        # job = self._make_job(url=micro_server_url)

        self._scheduler.add_job(
            self._make_monitor(url=micro_server_url, task_id=micro_server_name),
            "interval",
            seconds=second,
            id=micro_server_name,
        )

        self._micro_service_dict |= {micro_server_name: micro_server_url}

    def close(self, need_wait_job: bool = True):
        self._scheduler.print_jobs()
        self._scheduler.shutdown(wait=need_wait_job)

    def get_micro_service_url(self, micro_service_name) -> str:
        return self._micro_service_dict.get(micro_service_name, None)


# testing
# async def main():
#     testing = MonitorMicroServer()
#     testing.start()

#     testing.add_micro_server(
#         micro_server_name="testing",
#         micro_server_url="http://140.113.238.35:5000/",
#         second=1,
#     )

#     await asyncio.sleep(10)
#     testing.close(need_wait_job=False)
#     return


# import asyncio

# asyncio.run(main())
