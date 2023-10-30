import g4f
import asyncio
import time

_providers = [
    g4f.Provider.Bing,
    g4f.Provider.ChatBase,
    g4f.Provider.GptGo,
    g4f.Provider.You,
    g4f.Provider.Liaobots,
    g4f.Provider.Yqcloud,
]
# https://myapollo.com.tw/blog/begin-to-asyncio/


async def run_provider(provider: g4f.Provider.BaseProvider):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": "can you use chinese ?"}],
            provider=provider,
        )
        # print(f"{provider.__name__}:", response)
        return f"{provider.__name__}: {response}"
    except Exception as e:
        return f"{provider.__name__}:{e}"


async def to_task(provider):
    task = asyncio.create_task(run_provider(provider))
    return task


async def run_all():
    tasks = [to_task(provider) for provider in _providers]
    done, _ = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED,
        timeout=5,
    )

    # Retrieve and print the first completed task
    for task in done:
        result = task.result()
        if result:
            print(f"Response from {result.get_name()} is ready.")
            await result


# async def run_all():
#     calls = [run_provider(provider) for provider in _providers]
#     await asyncio.gather(*calls)


asyncio.run(run_all())
