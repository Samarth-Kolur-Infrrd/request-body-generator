import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost",
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

connection.close()