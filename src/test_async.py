import asyncio


async def job1():
    await asyncio.sleep(2)
    return "Result from job 1"


async def job2():
    await asyncio.sleep(1)
    return "Result from job 2"


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

        # Cancel remaining tasks
        for task in pending_tasks:
            task.cancel()

        # Get and print the result of the first completed task
        result = await completed_task.pop()
        print("Completed task:", result)
    except asyncio.CancelledError:
        print("Cancelled task:", task)


if __name__ == "__main__":
    asyncio.run(main())
