FROM python:3.11-slim

WORKDIR /app

# Dipendenze di sistema per confluent-kafka (librdkafka) e ssh client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        librdkafka-dev \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Copio il consumer e l'entrypoint
COPY entrypoint.sh /app/entrypoint.sh
COPY receiver.py /app/receiver.py

RUN chmod +x /app/entrypoint.sh

# Installo libreria Kafka
RUN pip install --no-cache-dir confluent-kafka

# Directory dove monteremo la chiave privata
RUN mkdir /ssh && chmod 700 /ssh

ENTRYPOINT ["/app/entrypoint.sh"]
