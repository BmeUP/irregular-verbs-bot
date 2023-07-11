FROM python:3.11-alpine
WORKDIR /app

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY src/ /app/src/
COPY iverbs.db /app/iverbs.db
COPY src/bot/irregular_verbs.json /app/src/bot/irregular_verbs.json

RUN pip install -r requirements.txt