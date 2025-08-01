from kafka import KafkaProducer
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")

producer = None

def get_producer():
    global producer
    if not producer:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                                 value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    return producer

def log_to_kafka(message: str):
    try:
        producer = get_producer()
        producer.send(KAFKA_TOPIC, {"message": message})
        producer.flush()
    except Exception as e:
        print(f"Error logging to Kafka: {e}")
