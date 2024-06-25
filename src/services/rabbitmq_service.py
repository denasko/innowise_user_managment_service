from base64 import urlsafe_b64encode
from datetime import datetime
from aio_pika.abc import AbstractRobustConnection
from pydantic import EmailStr
from src.core.schemas.message_reset_password import ResetPasswordMessage
from src.managers.rabbitmq_manager import RabbitMQManager


class RabbitMQService:
    def __init__(self, connection: AbstractRobustConnection):
        self.connection = connection
        self.rabbit_manager = RabbitMQManager(connection=connection)

    async def create_message_to_rabbitmq(self, queue: str, email: EmailStr):
        message: str = self.create_reset_password_message(email=email)
        return await self.rabbit_manager.publish_message_to_rabbitmq(queue=queue, message=message)

    @staticmethod
    def create_reset_password_message(email: str) -> str:
        encoded_email = urlsafe_b64encode(email.encode()).decode()
        link_for_reset_password = f"https://example.com/reset-password?{encoded_email}"

        email_subject = "Hello, it's me"
        body = f"Please use the following link to reset your password: {link_for_reset_password}"

        message = ResetPasswordMessage(
            email_subject=email_subject,
            body=body,
            published=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

        return message.json()
