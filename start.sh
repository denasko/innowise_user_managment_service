#!/bin/bash

alembic upgrade head
uvicorn src.core.main:app --host 0.0.0.0 --port 80 --reload
