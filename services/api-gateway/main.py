from fastapi import FastAPI

app = FastAPI(
    title="UdaConnect API Gateway",
    description="API Gateway for UdaConnect microservices architecture",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "UdaConnect API Gateway is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/locations")
def ingest_location(location: dict):
    """
    Endpoint to receive location data.
    In future phases, this will send data to Kafka.
    """
    return {
        "message": "Location received",
        "data": location
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

