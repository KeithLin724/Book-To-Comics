import g4f
import asyncio
import time

_providers = [
    g4f.Provider.Bing,
    g4f.Provider.ChatBase,
    g4f.Provider.GptGo,
    g4f.Provider.You,
    g4f.Provider.Yqcloud,
]
# https://myapollo.com.tw/blog/begin-to-asyncio/


async def run_provider(provider: g4f.Provider.BaseProvider):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": "can you use chinese ?"}],
            provider=provider,
            timeout=5,
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}:", e)


async def run_all():
    calls = [run_provider(provider) for provider in _providers]
    await asyncio.gather(*calls)


asyncio.run(run_all())
