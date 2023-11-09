import g4f
import asyncio
from enum import Enum

# https://myapollo.com.tw/blog/begin-to-asyncio/


class TextGenerator:
    """
    The `TextGenerator` class is a Python class that generates text using the GPT-4 model and multiple
    providers asynchronously."""

    class MessageState(Enum):
        ok = "OK"
        err = "ERR"

    G4F_VERSION = g4f.version

    def __init__(self) -> None:
        self._provide = [
            g4f.Provider.Bing,
            g4f.Provider.ChatBase,
            g4f.Provider.GptGo,
            g4f.Provider.You,
            # g4f.Provider.Yqcloud,
        ]

    async def run_provider(self, provider: g4f.Provider.BaseProvider, prompt: str):
        """
        The function `run_provider` takes a provider and a prompt as input, and uses the provider to
        generate a response to the prompt using the GPT-4 model.

        :param provider: The `provider` parameter is an instance of a class that inherits from
        `g4f.Provider.BaseProvider`. It is used to specify the provider for the chat completion model
        :type provider: g4f.Provider.BaseProvider
        :param prompt: The `prompt` parameter is a string that represents the user's input or message to the
        chatbot. It is the content that the user wants to send to the chatbot for processing
        :type prompt: str
        :return: The function `run_provider` returns a tuple containing three elements:
        """
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                provider=provider,
                timeout=5,
            )
            # print(f"{provider.__name__}:", response)
            return "OK", provider.__name__, response
        except Exception as e:
            return "ERR", provider.__name__, str(e)

    async def get_waiting(self, task_list: list):
        """
        The `get_waiting` function waits for the first task in a list to complete and returns its result
        along with the remaining pending tasks.

        :param task_list: The `task_list` parameter is a list of tasks that you want to wait for. These
        tasks are typically created using the `asyncio.create_task()` function or by wrapping a coroutine
        function with `asyncio.ensure_future()`. Each task represents a concurrent operation that you want
        to wait for
        :type task_list: list
        :return: The function `get_waiting` returns two values: `result` and `pending_tasks`.
        """
        try:
            # Wait for the first task to complete
            completed_task, pending_tasks = await asyncio.wait(
                task_list, return_when=asyncio.FIRST_COMPLETED
            )

            # Check the result of the first completed task
            result = await completed_task.pop()

            return result, pending_tasks
        except asyncio.CancelledError as e:
            print(e)
            pass

    async def get_generate(self, prompt: str):
        """
        The function `get_generate` takes a prompt as input and runs multiple providers asynchronously,
        returning the first successful result or the first error encountered.

        :param prompt: The `prompt` parameter is a string that represents the input prompt for
        generating text. It is used as an input for each provider in the `_provide` list
        :type prompt: str
        :return: a tuple containing the provider name and the generated message. If all tasks encounter
        an error, the function returns the first error encountered. If there are no pending tasks, an
        empty string is returned.
        """
        pending_tasks = [
            asyncio.create_task(
                self.run_provider(
                    provider=provider,
                    prompt=prompt,
                )
            )
            for provider in self._provide
        ]

        first_result = None
        # result, pending_tasks = await self.get_waiting(pending_tasks)
        for _ in range(len(pending_tasks)):
            result, pending_tasks = await self.get_waiting(pending_tasks)
            state, provider_name, msg = result

            if pending_tasks is None:
                return ""

            # is ok
            if state == "OK" and msg != "":
                for task in pending_tasks:
                    task.cancel()

                # [task.cancel() for task in pending_tasks]

                return provider_name, msg

            # handel error
            elif state == "ERR":
                first_result = result

        return first_result[-1]

    async def generate(self, prompt):
        """
        The function "generate" is an asynchronous function that takes a prompt as input and returns the
        result of calling the "get_generate" function with the prompt as an argument.

        :param prompt: The prompt is the input text or sentence that you want to use as a starting point
        for generating the output
        :return: The result of the `get_generate` method is being returned.
        """

        provider, msg = await self.get_generate(prompt=prompt)
        return provider, msg
