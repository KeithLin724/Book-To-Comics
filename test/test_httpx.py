import httpx
import asyncio


async def test_get():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("http://140.113.238.35:5000")

            print(res.status_code)
    except Exception as e:
        print(f"error {e}")


async def main():
    await test_get()


asyncio.run(main())
