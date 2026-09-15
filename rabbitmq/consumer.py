import pika
import json
import traceback
import os
import logging

from app.generator import generate_request_body

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ.get("RABBITMQ_HOST", "localhost"),
        port=5672,
        heartbeat=60
    )
)

logger = logging.getLogger(__name__)

channel = connection.channel()
 
def generator_queue(ch, method, properties, body):
    try:
        logger.info(" STARTING TO GENERATE THE REQUEST BODY ")

        input_id = json.loads(body)
        result = generate_request_body(input_id)
        logger.info(" GENERATED THE REQUESTBODY SUCCESSFULLY ")
        logger.info(" PUBLISHING A MESSAGE ON THE COMPLETED QUEUE ")

        channel.basic_publish(
            exchange = "generator.event",
            routing_key = "generator.completed",
            body = json.dumps(result, default=str),
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            )
        )
        logger.info(" MESSAGE PUBLISHED SUCCESSFULLY ")
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
    logger.info(" PROCESSING THE COMPLETED QUEUE ")
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
        logger.info(" FETCHING THE MESSAGE ")

        method, properties, body = channel.basic_get(
            queue="generator_completed",
            auto_ack=False
        )
    except (pika.exceptions.StreamLostError, pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed):
        logger.info(" RABBITMQ CONNECTION ERROR, TRYING TO RECONNECT... ")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get("RABBITMQ_HOST", "localhost"),
                port=5672,
                heartbeat=60
            )
        )
        logger.info(" cONNECTION ESTABLISHED ")

        channel = connection.channel()
        method, properties, body = channel.basic_get(
            queue="generator_completed",
            auto_ack=False
        )
        logger.info(" MESSAGE FETCHED ")

    if method is None:
        logger.info(" METHOD IS EMPTY ")
        return None

    try:
        result = json.loads(body)
        logger.info(" RETURNING THE REQUESTBODY ")
        channel.basic_ack(
            delivery_tag=method.delivery_tag
        )
        return result

    except Exception as e:
        logger.info("Fetching failed:", e)
        return None
    
if __name__ == "__main__":
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="generator_queue",
        on_message_callback=generator_queue,
        auto_ack=False
    )
    logger.info(" STARTING TO CONSUME ")
    channel.start_consuming()