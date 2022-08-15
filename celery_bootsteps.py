"""Module contains celery bootsteps 
which we can do custom actions at different 
stages in the worker """

from celery import bootsteps

from queues import get_queue_for_delayed_task_delivery


class DeclareQueueAndExchangeForDelayedTaskDelivery(bootsteps.StartStopStep):
    """
    Celery Bootstep to declare the exchange and queues for
    "Scheduling celery Task".
    """

    #  'bootsteps.StartStopStep': Bootsteps is a technique to add functionality
    #                             to the workers.A bootstep is a custom class
    #                             that defines hooks to do custom actions at different
    #                             stages in the worker.

    # The bootstep we have defined, require the Pool bootstep.
    # Pool: The current process/eventlet/gevent/thread pool
    requires = {"celery.worker.components:Pool"}

    def start(self, worker):
        queues_for_delayed_task_delivery = get_queue_for_delayed_task_delivery(
            destination_queue_name="delayed-add-tasks"
        )
        with worker.app.pool.acquire() as conn:
            queues_for_delayed_task_delivery.destination_queue.bind(conn).declare()
            queues_for_delayed_task_delivery.temp_queue_for_delayed_delivery.bind(
                conn
            ).declare()
