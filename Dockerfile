FROM python:3.11.4-slim-buster

ENV TZ="Europe/Moscow"
RUN apt-get update && apt-get install 
WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt