FROM python:3.12.3

WORKDIR /web_api

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY ./web_api /code/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]