from fastapi import FastAPI,Body
import uvicorn
import pika
import json
import time
import os
import logging

from rabbitmq.consumer import get_completed_request_body_from_queue

logger = logging.getLogger(__name__)

app = FastAPI()

params = pika.ConnectionParameters(
        host = os.environ.get("RABBITMQ_HOST", "localhost"),
        port = 5672,
        heartbeat=60
    )

connection = pika.BlockingConnection( params )

channel = connection.channel()

def publish_queued(input_id: dict):
    global connection, channel
    if connection.is_closed:
        connection = pika.BlockingConnection( params )
        channel = connection.channel()
    try:
        channel.basic_publish(
            exchange = "generator.event",
            routing_key = "generator.queued",
            body = json.dumps(input_id),
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
            body = json.dumps(input_id),
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            )
        )

@app.get("/requestGenerator/{document_id}")
async def request_generator(document_id: str) -> dict:
    logger.info("DOCUMENT ID RECIEVED")
    input_id = {"documentId": document_id}
    publish_queued(input_id)

    timeout = 10 
    poll_interval = 0.5
    waited = 0
    output_request = None
    while waited < timeout:
        output_request = get_completed_request_body_from_queue()
        if output_request is not None:
            break
        time.sleep(poll_interval)
        waited += poll_interval

    if output_request is None:
        logger.warning("SOMETHING WENT WRONG. REQUEST TIMEOUT")
        return {"result": "TIMEOUT"}
    
    return output_request
 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)