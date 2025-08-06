# kafka_consumer.py
from confluent_kafka import Consumer, KafkaException
from datetime import datetime
import json
import time

LOG_FILE = "kafka_messages.log"

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'log_reader',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})

consumer.subscribe(['logs'])

with open(LOG_FILE, "a") as f:
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            try:
                payload = json.loads(msg.value().decode('utf-8'))
            except Exception as e:
                payload = {"error": str(e), "raw": msg.value().decode('utf-8', errors='ignore')}

            log_entry = f"{datetime.now().isoformat()} - {json.dumps(payload)}"
            print("🔔", log_entry)
            f.write(log_entry + "\n")
    except KeyboardInterrupt:
        print("🛑 Stopping consumer...")
    finally:
        consumer.close()
