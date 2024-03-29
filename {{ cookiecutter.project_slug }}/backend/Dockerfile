FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements_fastapi.txt

EXPOSE 8000
