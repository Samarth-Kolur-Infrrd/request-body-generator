FROM python:3.12.3-slim

WORKDIR /app

COPY consumer.py .
COPY generator.py .
COPY mongoConnection.py .
COPY builders.py .

RUN pip install pika
RUN pip install pymongo
RUN pip install dotenv

CMD ["python","consumer.py"]