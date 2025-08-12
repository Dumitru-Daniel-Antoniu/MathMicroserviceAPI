import redis
import json
import os

REDIS_STREAM = os.getenv("REDIS_STREAM", "logs")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def log_to_redis_stream(message: dict):
    try:
        if not isinstance(message, dict):
            message = {"message": str(message)}
        
        message_clean = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in message.items()
        }
        redis_client.xadd(REDIS_STREAM, message_clean)
    except Exception as e:
        print(f"Error logging to Redis stream: {e}")

