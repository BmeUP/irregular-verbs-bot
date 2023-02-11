FROM python:3.11-alpine
WORKDIR /app

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY src/ /app/src/
COPY iverbs.db /app/iverbs.db
COPY list-of-irregular-verbs.pdf /app/src/list-of-irregular-verbs.pdf

RUN pip install -r requirements.txt