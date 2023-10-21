import queue
import threading

# Create a task queue
task_queue = queue.Queue()


# Define a worker function to process tasks
def worker():
    while True:
        try:
            task = task_queue.get(timeout=1)  # Get a task from the queue
            # Process the task here
            print(f"Processing task: {task}")
            task_queue.task_done()  # Mark the task as done
        except queue.Empty:
            # Handle the case where the queue is empty
            pass


# Create worker threads
num_workers = 4  # Adjust the number of worker threads as needed
threads = [threading.Thread(target=worker) for _ in range(num_workers)]

# Start the worker threads
for thread in threads:
    thread.start()

# Add tasks to the queue
for i in range(10):
    task_queue.put(f"Task {i}")

# Wait for all tasks to be processed
task_queue.join()

# Stop the worker threads (in a production scenario, use a proper termination signal)
for thread in threads:
    thread.join()
