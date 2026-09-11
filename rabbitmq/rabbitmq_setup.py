import pika
import os 
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST", "localhost"),
                              port=5672,
                              heartbeat=60)
)

channel = connection.channel()

channel.exchange_declare(
    exchange="generator.event",
    exchange_type="topic",
    durable=True
)

channel.queue_declare(
    queue="generator_queue",
    durable=True
)

channel.queue_bind(
    exchange="generator.event",
    queue="generator_queue",
    routing_key="generator.queued"
)

channel.queue_declare(
    queue="generator_completed",
    durable=True
)

channel.queue_bind(
    exchange="generator.event",
    queue="generator_completed",
    routing_key="generator.completed"

)
connection.close()