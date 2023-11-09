from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from apscheduler.events import EVENT_JOB_ERROR

from . import LOGGER

# https://apscheduler.readthedocs.io/en/3.x/userguide.html
import httpx


class MonitorMicroServer:
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()
        self._micro_service_dict = {}

    def start(self):
        self._scheduler.start()

    def _make_monitor(self, url: str, task_id: str, is_alive_root: str):
        """
        The `_make_monitor` function creates an asynchronous function `get_alive` that sends a GET request
        to a specified URL and prints the response status code, or an error message if the request fails.

        :param url: The `url` parameter is a string that represents the URL of a micro service that you want
        to monitor
        :type url: str
        :param task_id: The `task_id` parameter is a string that represents the unique identifier for a
        specific task or job. It is used to identify and manage the task within the `_micro_service_dict`
        dictionary and the `_scheduler` object
        :type task_id: str
        :return: The function `_make_monitor` returns an asynchronous function `get_alive`.
        """

        async def get_alive() -> None:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(f"{url}/{is_alive_root}")

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
        micro_server_is_alive_root: str,
        micro_server_method_root: str,
        second: int = 5,
    ) -> None:
        """The `add_micro_server` function adds a micro server to a scheduler with a specified name, URL,
        and interval for checking its availability.

        Parameters
        ----------
        micro_server_name : str
            The `micro_server_name` parameter is a string that represents the name or identifier of the
        micro server.
        micro_server_url : str
            The `micro_server_url` parameter is the URL of the micro server that you want to add to the
        scheduler. It is a string that represents the address of the micro server.
        micro_server_is_alive_root : str
            The parameter `micro_server_is_alive_root` is the root endpoint or URL path that indicates
        whether the micro server is alive or not. It is used by the monitoring task to check the health
        status of the micro server.
        second : int, optional
            The `second` parameter is an optional parameter that specifies the interval in seconds at which
        the micro server should be monitored. If not provided, it defaults to 5 seconds.

        """
        self._scheduler.add_job(
            self._make_monitor(
                url=micro_server_url,
                task_id=micro_server_name,
                is_alive_root=micro_server_is_alive_root,
            ),
            "interval",
            seconds=second,
            id=micro_server_name,
        )

        self._micro_service_dict |= {
            micro_server_name: {
                "url": micro_server_url,
                "method": micro_server_method_root,
            }
        }

    def close(self, need_wait_job: bool = True, out=print):
        """
        The `close` function removes all scheduled jobs from the scheduler and shuts it down, optionally
        waiting for any running jobs to finish.

        :param need_wait_job: The `need_wait_job` parameter is a boolean flag that determines whether the
        program should wait for all scheduled jobs to finish before shutting down. If `need_wait_job` is set
        to `True`, the program will wait for all jobs to finish before shutting down. If `need_wait_job` is,
        defaults to True
        :type need_wait_job: bool (optional)
        :param out: The `out` parameter is a function that is used to specify where the output should be
        directed. By default, it is set to the `print` function, which means that the output will be printed
        to the console. However, you can pass a different function to the `out` parameter if
        """
        # self._scheduler.print_jobs()
        jobs = self._scheduler.get_jobs()
        display = ", ".join(jobs) if len(jobs) != 0 else "empty"
        out(f"schedule Jobs : {display}")
        self._scheduler.remove_all_jobs()
        self._scheduler.shutdown(wait=need_wait_job)

    def get_micro_service_url(self, micro_service_name: str) -> str:
        """The function `get_micro_service_url` returns the URL of a microservice based on its name.

        Parameters
        ----------
        micro_service_name
            The `micro_service_name` parameter is a string that represents the name of a microservice.

        Returns
        -------
            a string, which is the URL of the microservice corresponding to the given micro_service_name. If
        the micro_service_name is not found in the _micro_service_dict, it returns None.

        """
        res = self._micro_service_dict.get(micro_service_name, None)
        return res["url"] if res is not None else None

    def get_micro_service_method_name(self, micro_service_name: str) -> str:
        """The function `get_micro_service_method` returns the method associated with a given micro service
        name from a dictionary.

        Parameters
        ----------
        micro_service_name
            The `micro_service_name` parameter is a string that represents the name of a microservice.

        Returns
        -------
            The method returns a string value.

        """
        res = self._micro_service_dict.get(micro_service_name, None)
        return res["method"] if res is not None else None

    def get_micro_service_method_url(self, micro_service_name: str) -> str:
        """The function `get_micro_service_method_url` returns the URL of a microservice method based on the
        microservice name.

        Parameters
        ----------
        micro_service_name : str
            The `micro_service_name` parameter is a string that represents the name of a microservice.

        Returns
        -------
            The method is returning a string that represents the URL of a microservice method.

        """
        res = self._micro_service_dict.get(micro_service_name, None)
        url, method_root = res["url"], res["method"]
        return f"{url}/{method_root}" if res is not None else None

    def get_all_micro_service(self):
        """
        The function returns a dictionary containing all microservices.
        :return: The method is returning the `_micro_service_dict` attribute.
        """
        return self._micro_service_dict

    def __contains__(self, key):
        return key in self._micro_service_dict


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
#     url = testing.get_micro_service_url("testing")
#     print(url)
#     testing.close(need_wait_job=False)
#     return


# import asyncio

# asyncio.run(main())
