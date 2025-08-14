import redis
import json
import os

"""
Redis stream logging utilities for FastAPI applications.

Provides functions to log structured messages to a Redis stream, supporting
customizable stream name and connection parameters via environment variables.
"""

REDIS_STREAM = os.getenv("REDIS_STREAM", "logs")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def log_to_redis_stream(message: dict):
    """
    Log a message to the configured Redis stream.

    Converts the message to a dictionary, serializes nested data
    and appends it to the Redis stream. Handles errors gracefully.

    Args:
        message (dict): Structured log message to send to Redis stream.
    """

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
