"""
Redis stream consumer for logging messages to a file.

Continuously reads messages from a Redis stream using a consumer group,
writes each message to a log file with a timestamp, and acknowledges
processed messages. Configurable via environment variables.
"""

import json
import os
import redis
import logging
from datetime import datetime


def consumer():
    """
    Start the Redis stream consumer.

    Initializes the Redis client and consumer group, reads messages from
    the configured stream, logs them to a file with timestamps, and
    acknowledges each message. Handles graceful shutdown on interruption.
    """

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    REDIS_STREAM = os.getenv("REDIS_STREAM", "logs")
    GROUP_NAME = "log_reader_group"
    CONSUMER_NAME = "log_consumer_1"
    LOG_FILE = "redis_messages.log"

    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
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
            logging.info("Consumer group already exists.")
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

                logging.info("Data processed")

                for stream, messages in response:
                    for msg_id, msg_data in messages:
                        current_date = datetime.now().isoformat()
                        data = json.dumps(msg_data)
                        log_entry = f"{current_date} - {data}"
                        f.write(log_entry + "\n")
                        f.flush()
                        redis_client.xack(
                            REDIS_STREAM,
                            GROUP_NAME,
                            msg_id
                        )

        except KeyboardInterrupt:
            logging.info("Stopping consumer...")


if __name__ == "__main__":
    consumer()
