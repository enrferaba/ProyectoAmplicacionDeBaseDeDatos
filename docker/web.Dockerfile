FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

WORKDIR /code/app

RUN python manage.py collectstatic --noinput || true

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
