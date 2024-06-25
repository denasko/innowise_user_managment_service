from pika.adapters.blocking_connection import BlockingConnection
import aio_pika


class RabbitMQManager:
    def __init__(self, connection: BlockingConnection):
        self.connection = connection

    async def publish_message_to_rabbitmq(self, queue: str, message: str) -> dict:
        async with self.connection.channel() as channel:
            await channel.declare_queue(queue, durable=True)
            await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=queue)
        return {"detail": "message has been sent"}
