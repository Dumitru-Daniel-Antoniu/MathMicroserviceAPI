from kafka import KafkaProducer
import json
import os
import time

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")

producer = None

def get_producer():
    global producer
    if not producer:
        try:
            print("Creating Kafka producer...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("Kafka producer created successfully.")
        except Exception as e:
            print(f"Error creating Kafka producer: {e}")
    return producer


def log_to_kafka(message: dict):
    try:
        producer = get_producer()
        print("Sending message to Kafka:", message)
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print("Kafka acknowledged")
    except Exception as e:
        print(f"Error logging to Kafka: {e}")
    