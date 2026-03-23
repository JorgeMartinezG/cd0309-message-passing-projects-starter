import json
from fastapi import FastAPI
from kafka import KafkaProducer

app = FastAPI(
    title="Location Ingestion Service",
    description="Receives location data and publishes it to Kafka",
    version="1.0.0"
)

KAFKA_TOPIC = "locations"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


@app.post("/locations")
def ingest_location(location: dict):
    """
    Receives location data and sends it to Kafka.
    """
    producer = get_kafka_producer()
    producer.send(KAFKA_TOPIC, location)
    producer.flush()

    return {
        "message": "Location sent to Kafka",
        "data": location
    }
