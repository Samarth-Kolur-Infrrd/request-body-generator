from fastapi import FastAPI,Body
import uvicorn
import pika
import json
import time
import os

from rabbitmq.consumer import getCompletedRequestBodyFromQueue

app = FastAPI()

params = pika.ConnectionParameters(
        host = os.environ.get("RABBITMQ_HOST", "localhost"),
        port = 5672,
        heartbeat=60
    )

connection = pika.BlockingConnection( params )

channel = connection.channel()

def publish_queued(inputId: dict):
    global connection, channel
    if connection.is_closed:
        connection = pika.BlockingConnection( params )
        channel = connection.channel()
    try:
        channel.basic_publish(
            exchange = "generator.event",
            routing_key = "generator.queued",
            body = json.dumps(inputId),
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            )
        )
    except (pika.exceptions.StreamLostError, pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed):
        connection = pika.BlockingConnection( params )
        channel = connection.channel()
        channel.basic_publish(
            exchange = "generator.event",
            routing_key = "generator.queued",
            body = json.dumps(inputId),
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            )
        )

@app.get("/requestGenerator/{document_id}")
async def requestgenerator(document_id: str) -> dict:
    inputId = {"documentId": document_id}
    publish_queued(inputId)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)