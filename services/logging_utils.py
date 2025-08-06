from confluent_kafka import Producer
import json
import os
import time

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")

producer = None

def delivery_report(err, msg):
    if err is not None:
        print(f"Kafka delivery failed: {err}")
    else:
        print(f"Kafka message delivered to {msg.topic()} [{msg.partition()}]")

def get_producer():
    global producer
    if not producer:
        try:
            print("Creating Kafka producer...")
            producer = Producer({
                'bootstrap.servers': KAFKA_BROKER,
                'client.id': f'producer_{int(time.time())}',
                'on_delivery': delivery_report
            })
            print("Kafka producer created successfully.")
        except Exception as e:
            print(f"Error creating Kafka producer: {e}")
    return producer


def log_to_kafka(message: dict):
    try:
        producer = get_producer()
        print("Sending message to Kafka:", message)
        producer.produce(
            KAFKA_TOPIC,
            key=str(int(time.time())),
            value=json.dumps(message),
            callback=delivery_report
        )
        producer.flush()
        print("Kafka acknowledged")
    except Exception as e:
        print(f"Error logging to Kafka: {e}")
    