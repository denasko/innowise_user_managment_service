FROM python:3.12

WORKDIR /app

RUN pip install poetry \
    && poetry config virtualenvs.create false \

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-interaction --no-ansi

COPY . /app

CMD ["uvicorn", "src.user_management_service.main:app", "--host", "0.0.0.0", "--port", "80"]
