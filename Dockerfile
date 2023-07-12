FROM python:3.11-alpine
WORKDIR /app

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY src/ /app/src/
COPY src/bot/irregular_verbs.json /app/src/bot/irregular_verbs.json
COPY ./entry.sh /app/entry.sh

RUN pip install -r requirements.txt
RUN chmod +x /app/entry.sh

ENTRYPOINT ["/app/entry.sh"]