import redis

# Replace these values with your Redis server configuration
redis_host = "localhost"  # Change this to your Redis server's host
redis_port = 6379  # Change this to your Redis server's port

try:
    # Create a Redis client
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    # Check if the connection is successful
    r.ping()

    print("Connected to Redis successfully.")
except redis.exceptions.ConnectionError as e:
    print(f"Error connecting to Redis: {e}")
