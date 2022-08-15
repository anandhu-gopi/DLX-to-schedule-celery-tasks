"""Module provides Celery app and configurations."""

import celery

from celery_bootsteps import DeclareQueueAndExchangeForDelayedTaskDelivery
from config import config
from queues import get_queue_for_delayed_task_delivery


class CeleryConfig:

    # Adding 'temp queue' to the task_queues.
    # otherwise, moving messages to the same will fail with
    # amqp.exceptions.PreconditionFailed error

    queues_for_delayed_task_delivery = get_queue_for_delayed_task_delivery(
        destination_queue_name="add-tasks"
    )
    task_queues = (queues_for_delayed_task_delivery.temp_queue_for_delayed_delivery,)

    broker_url = "{protocol}://{username}:{password}@{host}:{port}/{vhost}".format(
        protocol=config.RABBITMQ_PROTOCOL,
        username=config.RABBIT_MQ_USERNAME,
        password=config.RABBIT_MQ_PSWD,
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        vhost=config.RABBITMQ_VHOST_FOR_CELERY,
    )

    # include: list of modules to import when the worker starts.
    #          we need to add our tasks module here
    #          so that the worker is able to find our tasks.
    include = ["tasks"]
    # task_routes: enables you to route tasks by name
    task_routes = {
        "add": {"queue": "add-tasks"},
    }

    # worker_send_task_event: We don't want celery to send each
    # and every task-related events, (for better performance)
    worker_send_task_event = False

    # By ignoring the task result, we can improve
    # the performance of the application
    task_ignore_result = True

    # task messages will be acknowledged after
    # the task has been executed,
    # not just before (the default behavior) ,
    # this we are doing for better reliability
    # (handling unexpected shutdown, power failure...)
    task_acks_late = True


app = celery.Celery("My_Celery")
app.config_from_object(CeleryConfig)

# adding new bootsteps to the worker that declare
# Queue and Exchange For Delayed-Delivery-Task,
app.steps["worker"].add(DeclareQueueAndExchangeForDelayedTaskDelivery)
