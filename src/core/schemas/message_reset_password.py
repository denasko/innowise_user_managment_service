from pydantic import BaseModel


class ResetPasswordMessage(BaseModel):
    email_subject: str
    body: str
    published: str
