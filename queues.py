"""Queues module provides the queues and exchanges for the celery tasks."""

from typing import NamedTuple

from kombu import Exchange, Queue


class QueuesForDelayedTaskDelivery(NamedTuple):
    destination_queue: Queue
    temp_queue_for_delayed_delivery: Queue


def get_queue_for_delayed_task_delivery(
    destination_queue_name: str,
) -> QueuesForDelayedTaskDelivery:
    """
    For setting up a queue using which we can delay
    the delivery of a task to the destination-queue
    for a certain time so that subscribers doesn't
    see them immediately.

    We will combine per-message-TTL and DLX (dead-letter-exchange)
    to delay task delivery.By combining these to functions we publish a
    message to a queue which will expire its message after the TTL
    and then reroute it to the destination queue and with the dead-letter
    routing key so that they end up in a queue which we consume from.

    (Per-message-TTL has to be set while invoking the task,
    see: https://stackoverflow.com/questions/26990438/how-to-set-per-message-expiration-ttl-in-celery )

    """
    EXCHANGE_TYPE: str = "direct"

    # * Like celery creates the queue and exchange with the same name,
    # * we will also create exchanges and queues with same name.
    temp_exchange_name = temp_queue_name = f"temp-{destination_queue_name}"
    destination_exchange_name = destination_queue_name

    # defining destination queue and exchange.
    destination_exchange = Exchange(
        destination_exchange_name,
        type=EXCHANGE_TYPE,
    )
    # max-retry-exceeded-queue-for-scan-doc-task-queue
    destination_queue = Queue(
        destination_queue_name,
        exchange=destination_exchange,
        routing_key=destination_queue_name,
    )

    # Steps to create temp_queue_for_delayed_delivery:
    #   1. Add the x-dead-letter-exchange argument property,
    #      and set it to the name of destination queue exchange.
    # 	2. Add the x-dead-letter-routing-key argument property,
    #      and set it to the name of the destination queue.
    #   3. Once messages from temp_queue_for_delayed_delivery, expires due
    #      to per-message TTL,they will be forwarded to the destination
    #      queue,and we will be able to achieve delayed task delivery.
    dead_letter_queue_args_for_temp_queue = {
        "x-dead-letter-exchange": destination_exchange_name,
        "x-dead-letter-routing-key": destination_queue_name,
    }

    temp_exchange_for_delayed_delivery = Exchange(
        temp_exchange_name,
        type=EXCHANGE_TYPE,
    )

    temp_queue_for_delayed_delivery = Queue(
        temp_queue_name,
        exchange=temp_exchange_for_delayed_delivery,
        routing_key=temp_queue_name,
        queue_arguments=dead_letter_queue_args_for_temp_queue,
    )
    return QueuesForDelayedTaskDelivery(
        destination_queue=destination_queue,
        temp_queue_for_delayed_delivery=temp_queue_for_delayed_delivery,
    )
