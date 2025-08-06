# kafka_consumer.py
import json
import time
import os
from confluent_kafka import Consumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")

consumer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': f"log_reader_{int(time.time())}",
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC])

LOG_FILE = "kafka_messages.log"

def write_to_log_file(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

try:
    print("Log consumer started. Waiting for messages...")
    while True:
        message = consumer.poll(2.0)
        if message is None:
            continue
        if message.error():
            print(f"Error: {message.error()}")
            continue

        try:
            value = message.value().decode('utf-8')
            data = json.loads(value)
            write_to_log_file(json.dumps(data, indent=2))
            consumer.commit()
        except Exception as e:
            print(f"Error processing message: {e}")

except KeyboardInterrupt:
    print("Shutting down consumer...")

finally:
    consumer.close()