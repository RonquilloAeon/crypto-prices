import logging
import os
import sys
import time
from typing import Any

from confluent_kafka import Producer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

TOPIC = "dev.machine.cpu"

p = Producer(
    {
        "bootstrap.servers": "0.0.0.0:9092",
        "group.id": "devgroup",
        "auto.offset.reset": "earliest",
    }
)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error('Message delivery failed: %s', err)
    else:
        logger.info('Message delivered to %s [%s]', msg.topic(), msg.partition())


def publish_message(data: Any):
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    logger.info("Publishing: %s", data)
    p.produce(TOPIC, str(data).encode('utf-8'), callback=delivery_report)

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    r = p.flush(timeout=5)

    if r > 0:
        logger.error('❌ Message delivery failed (%s message(s) still remain)', r)


def get_cpu_load() -> int:
    # See
    # https://medium.com/the-andela-way/\
    # machine-monitoring-tool-using-python-from-scratch-8d10411782fd
    return [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]


if __name__ == "__main__":
    try:
        while True:
            cpu_load = get_cpu_load()
            publish_message(cpu_load)

            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
