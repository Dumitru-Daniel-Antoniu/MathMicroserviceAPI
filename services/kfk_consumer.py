# kafka_consumer.py
from kafka import KafkaConsumer
from datetime import datetime
import json
import time

LOG_FILE = "kafka_messages.log"

def safe_json_deserializer(m):
    try:
        return json.loads(m.decode("utf-8"))
    except Exception as e:
        print(f"⚠️ Deserialization failed: {e}")
        return {"raw": m.decode("utf-8")}

consumer = KafkaConsumer(
    'logs',
    bootstrap_servers='localhost:9092',
    group_id=f"log_reader_{int(time.time())}",
    auto_offset_reset='earliest',
    value_deserializer=safe_json_deserializer,
    enable_auto_commit=False
)

print("Listening for Kafka logs...")

with open(LOG_FILE, "a") as f:
    while True:
        print("Polling...")
        raw_messages = consumer.poll(timeout_ms=2000)
        print("Received batch:", raw_messages)
        for _, msg_list in raw_messages.items():
            for msg in msg_list:
                print("🔔 MESSAGE:", msg.value)
