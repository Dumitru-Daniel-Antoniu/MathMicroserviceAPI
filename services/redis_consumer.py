# kafka_consumer.py
from datetime import datetime
import json
import os
import redis

REDIS_STREAM = os.getenv("REDIS_STREAM", "logs")
GROUP_NAME = "log_reader_group"
CONSUMER_NAME = "log_consumer_1"
LOG_FILE = "redis_messages.log"

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

try:
    redis_client.xgroup_create(
        REDIS_STREAM,
        GROUP_NAME,
        id='0',
        mkstream=True
    )
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP" in str(e):
        print("Consumer group already exists.")
    else:
        raise

with open(LOG_FILE, "a") as f:
    try:
        while True:
            response = redis_client.xreadgroup(
                GROUP_NAME,
                CONSUMER_NAME,
                {REDIS_STREAM: '>'},
                count=10,
                block=5000
            )

            for stream, messages in response:
                for msg_id, msg_data in messages:
                    log_entry = f"{datetime.now().isoformat()} - {json.dumps(msg_data)}"
                    print("🔔", log_entry)
                    f.write(log_entry + "\n")
                    # Acknowledge processing
                    redis_client.xack(
                        REDIS_STREAM,
                        GROUP_NAME,
                        msg_id
                    )
    except KeyboardInterrupt:
        print("🛑 Stopping consumer...")
