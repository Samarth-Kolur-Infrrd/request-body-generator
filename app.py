from fastapi import FastAPI,Body
import uvicorn
import pika
import json
import time
import os

from generator import generateRequestBody
from consumer import getCompletedRequestBodyFromQueue

app = FastAPI()

params = pika.ConnectionParameters(
        host = os.environ.get("RABBITMQ_HOST", "localhost"),
        port = 5672,
        heartbeat=60
    )

connection = pika.BlockingConnection( params )

channel = connection.channel()

@app.get("/requestGenerator/{document_id}")
async def requestgenerator(document_id: str):
    inputId = {"documentId": document_id}
    channel.basic_publish(
        exchange = "generator.event",
        routing_key = "generator.queued",
        body = json.dumps(inputId),
        properties = pika.BasicProperties(
            delivery_mode = pika.DeliveryMode.Persistent
        )
    )

    timeout = 10 
    poll_interval = 0.5
    waited = 0
    outputRequest = None
    while waited < timeout:
        outputRequest = getCompletedRequestBodyFromQueue()
        if outputRequest is not None:
            break
        time.sleep(poll_interval)
        waited += poll_interval

    if outputRequest is None:
        return {"result": "TIMEOUT"}
    
    return outputRequest

if __name__ == "__main__":
    uvicorn.run(app)