import pika
import json
import traceback
import os

from app.generator import generate_request_body

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ.get("RABBITMQ_HOST", "localhost"),
        port=5672,
        heartbeat=60
    )
)

channel = connection.channel()
 
def generator_queue(ch, method, properties, body):
    try:
        print("Inside the queue, preparing to generate request body")
        input_id = json.loads(body)
        result = generate_request_body(input_id)
        print("Request Body generated successfuly. Now publishing it into completed queue")
        channel.basic_publish(
            exchange = "generator.event",
            routing_key = "generator.completed",
            body = json.dumps(result, default=str),
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            )
        )
        print("Published successfully!")
        channel.basic_ack(
            delivery_tag = method.delivery_tag
        )
    except Exception as e:
        traceback.print_exc()
        print("Processing Failed")
        channel.basic_nack(
            delivery_tag = method.delivery_tag,
            requeue = False
        )


def get_completed_request_body_from_queue():
    global connection, channel
    print("Inside the completed queue, preparing to return the generated request body")

    result = None

    if connection.is_closed:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get("RABBITMQ_HOST", "localhost"),
                port=5672,
                heartbeat=60
            )
        )
        channel = connection.channel()

    try:
        method, properties, body = channel.basic_get(
            queue="generator_completed",
            auto_ack=False
        )
    except (pika.exceptions.StreamLostError, pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get("RABBITMQ_HOST", "localhost"),
                port=5672,
                heartbeat=60
            )
        )
        channel = connection.channel()
        method, properties, body = channel.basic_get(
            queue="generator_completed",
            auto_ack=False
        )

    if method is None:
        return None

    try:
        result = json.loads(body)
        print("Returning result")
        
        channel.basic_ack(
            delivery_tag=method.delivery_tag
        )
        return result

    except Exception as e:
        print("Fetching failed:", e)
        return None
    
if __name__ == "__main__":
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="generator_queue",
        on_message_callback=generator_queue,
        auto_ack=False
    )
    print("Starting to consume")
    channel.start_consuming()