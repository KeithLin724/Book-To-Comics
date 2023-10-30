import asyncio


async def job1():
    await asyncio.sleep(2)
    return "bad_news_1"


async def job2():
    await asyncio.sleep(1)
    return "bad_news"


async def job3():
    await asyncio.sleep(3)
    return "Result from job 3"


async def main():
    tasks = [job1(), job2(), job3()]

    # Create asyncio.Task instances from coroutines
    task_list = [asyncio.create_task(task) for task in tasks]

    try:
        # Wait for the first task to complete
        completed_task, pending_tasks = await asyncio.wait(
            task_list, return_when=asyncio.FIRST_COMPLETED
        )

        # Check the result of the first completed task
        result = await completed_task.pop()
        if result == "bad_news":
            # If the result is "bad_news," await the second task
            second_completed_task, _ = await asyncio.wait(
                pending_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            result = await second_completed_task.pop()
        else:
            # Cancel the remaining tasks
            for task in pending_tasks:
                task.cancel()

        print("Completed task:", result)
    except asyncio.CancelledError:
        print("Cancelled task:", task)


if __name__ == "__main__":
    asyncio.run(main())
