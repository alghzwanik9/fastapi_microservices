import pika
import json
from ..utils.config import get_settings

settings = get_settings()


def get_rabbitmq_connection():
    """Create and return a RabbitMQ connection."""
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    return connection


def publish_event(routing_key: str, message: dict):
    """Publish an event to RabbitMQ exchange."""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declare exchange
        channel.exchange_declare(
            exchange=settings.RABBITMQ_EXCHANGE,
            exchange_type='topic',
            durable=True
        )

        # Publish message
        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )

        connection.close()
        print(f"Event published: {routing_key} - {message}")
    except Exception as e:
        print(f"Error publishing event: {e}")


def consume_events(queue_name: str, callback_function, routing_keys: list):
    """Consume events from RabbitMQ queue."""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declare exchange
        channel.exchange_declare(
            exchange=settings.RABBITMQ_EXCHANGE,
            exchange_type='topic',
            durable=True
        )

        # Declare queue
        channel.queue_declare(queue=queue_name, durable=True)

        # Bind queue to routing keys
        for routing_key in routing_keys:
            channel.queue_bind(
                exchange=settings.RABBITMQ_EXCHANGE,
                queue=queue_name,
                routing_key=routing_key
            )

        # Set up consumer
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback_function,
            auto_ack=True
        )

        print(f"[*] Waiting for messages in {queue_name}. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Error consuming events: {e}")
