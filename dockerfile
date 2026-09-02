FROM python:3.12.3-slim

WORKDIR /app

COPY app.py .
COPY consumer.py .
COPY generator.py .
COPY mongoConnection.py .
COPY builders.py .
COPY rabbitmqSetup.py .

RUN pip install pika
RUN pip install pymongo
RUN pip install dotenv
RUN pip install fastapi
RUN pip install uvicorn

ENV PYTHONUNBUFFERED=1

CMD ["python","consumer.py"]