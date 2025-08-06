from confluent_kafka import Producer
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")

producer = None


def get_producer():
    global producer
    if not producer:
        try:
            print("Creating Kafka producer...")
            producer_config = {
                'bootstrap.servers': KAFKA_BROKER
            }
            producer = Producer(producer_config)
            print("Kafka producer created successfully.")
        except Exception as e:
            print(f"Error creating Kafka producer: {e}")
    return producer


def log_to_kafka(message: dict):
    try:
        producer = get_producer()
        print("Sending message to Kafka:", message)
        message = json.dumps(message).encode('utf-8')
        producer.produce(KAFKA_TOPIC, value=message)
        producer.flush()
        print("Kafka acknowledged")
    except Exception as e:
        print(f"Error logging to Kafka: {e}")
