import pika
import json
import traceback
import os


from generator import generateRequestBody

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ.get("RABBITMQ_HOST", "localhost"),
        port=5672
    )
)

channel = connection.channel()
 
def generatorQueue(ch, method, properties, body):
    try:
        print("Inside the queue, preparing to generate request body")
        inputId = json.loads(body)
        result = generateRequestBody(inputId)
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


def getCompletedRequestBodyFromQueue():
    print("Inside the completed queue, preparing to return the generated request body")

    result = None

    method, properties, body = channel.basic_get(
        queue="generatorCompleted",
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
        queue="generatorQueue",
        on_message_callback=generatorQueue,
        auto_ack=False
    )
    print("Starting to consume")
    channel.start_consuming()