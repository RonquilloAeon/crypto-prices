import logging
import sys

from confluent_kafka import Consumer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

TOPIC = "crypto.candles"

c = Consumer(
    {
        "bootstrap.servers": "0.0.0.0:9092",
        "group.id": "devgroup",
        "auto.offset.reset": "earliest",
    }
)


if __name__ == "__main__":
    c.subscribe([TOPIC])

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                logger.error("Error: %s", msg.error())

            logger.info("Received: %s", str(msg.value().decode("utf-8")))
    except KeyboardInterrupt:
        c.close()
        sys.exit(0)
