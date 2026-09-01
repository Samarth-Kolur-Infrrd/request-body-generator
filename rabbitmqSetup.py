import pika
import os 
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST", "localhost"),
                              port=5672)
)

channel = connection.channel()

channel.exchange_declare(
    exchange="generator.event",
    exchange_type="topic",
    durable=True
)

channel.queue_declare(
    queue="generatorQueue",
    durable=True
)

channel.queue_bind(
    exchange="generator.event",
    queue="generatorQueue",
    routing_key="generator.queued"
)

channel.queue_declare(
    queue="generatorCompleted",
    durable=True
)

channel.queue_bind(
    exchange="generator.event",
    queue="generatorCompleted",
    routing_key="generator.completed"

)
connection.close()