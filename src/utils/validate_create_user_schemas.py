from dataclasses import dataclass
from typing import Any

from fastapi import Form
from pydantic import ValidationError

from src.core.exeption_handlers import ValidationException
from src.core.schemas.user import UserCreate


@dataclass
class CreateUser:
    name: Any = (Form(...),)
    surname: Any = (Form(...),)
    username: Any = (Form(...),)
    phone_number: Any = (Form(...),)
    email: Any = (Form(...),)
    role: Any = (Form(...),)
    image_s3_path: Any = (Form(...),)
    password: Any = (Form(...),)
    group_id: Any = (Form(...),)


def new_user_to_pydantic_schema(new_user: CreateUser) -> UserCreate:
    try:
        user_pydantic = UserCreate(
            name=new_user.name,
            surname=new_user.surname,
            username=new_user.username,
            phone_number=new_user.phone_number,
            email=new_user.email,
            role=new_user.role,
            image_s3_path=new_user.image_s3_path,
            password=new_user.password,
            group_id=new_user.group_id,
        )
    except ValidationError as e:
        raise ValidationException(detail=e.errors())
    return user_pydantic
