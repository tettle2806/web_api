FROM python:3.12.3
LABEL authors="Rasulov Zayniddin"

WORKDIR ./app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app


RUN pip install -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]