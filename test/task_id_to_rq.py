import redis
from rq.job import Job

# 连接到Redis服务器
redis_conn = redis.Redis(host="140.113.238.35", port=6379)
job_id = input("id:")
# 创建RQ队列
# queue = Queue(connection=redis_conn)

# # 获取任务ID，可以从请求上下文或其他方式获取
# # 这里使用get_current_job()来获取当前任务的ID，实际中可以根据您的需要获取任务ID
# job_id = get_current_job().id

# 使用任务ID获取任务对象
job = Job.fetch(job_id, connection=redis_conn)

# 获取任务的执行结果
result = job.result  # 这将阻塞，直到任务完成

# 输出任务的结果
print("Task result:", result)
