FROM python:3.12

WORKDIR /app

RUN pip install poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-interaction --no-ansi

COPY . /app

COPY start.sh /app/start.sh

RUN chmod a+x /app/start.sh

CMD ["./start.sh"]
