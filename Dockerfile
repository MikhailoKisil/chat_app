FROM python:3.11-alpine3.16

COPY requirements.txt /temp/requirements.txt
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt
COPY . /chat_app

WORKDIR /chat_app

EXPOSE 8000

RUN adduser --disabled-password chat-user

USER chat-user