import json
from kafka import KafkaConsumer

KAFKA_TOPIC = "locations"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def start_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("Location Processing Service started. Waiting for messages...")

    for message in consumer:
        location = message.value
        process_location(location)


def process_location(location: dict):
    """
    Process incoming location data.
    In a real scenario, this would store data in a database.
    """
    print(f"Processing location: {location}")


if __name__ == "__main__":
    start_consumer()
