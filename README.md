# kafka-dev
Kafka Dev Setup

## Get started
- Run `docker-compose up` to start Kafka
- In a new tab, run `python producer.py`
- In another tab, run `python consumer.py`

If you have strange issues w/ Kafka, you may need to increase the Docker memory allocation
to 8GB.

## Kafka Connect
You can add connectors to Kafka Connect by placing the JAR(s) in `.connect/jars`.
