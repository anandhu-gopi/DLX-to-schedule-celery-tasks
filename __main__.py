from queues import QueuesForDelayedTaskDelivery, get_queue_for_delayed_task_delivery
from tasks import add

if __name__ == "__main__":

    queues_for_delayed_task_delivery: QueuesForDelayedTaskDelivery = (
        get_queue_for_delayed_task_delivery(destination_queue_name="delayed-add-tasks")
    )
    add.apply_async(  # kwargs: eqivalent to calling add(a=1,b=2)
        kwargs={"a": 1, "b": 2},
        # Moving task to the temp-queue (for delayed-task-delivery),
        # Once tasks from temp_queue_for_delayed_delivery, expires due
        # to TTL,they will be forwarded to the destination queue,
        # and we will be able to achieve delayed task delivery.
        queue=queues_for_delayed_task_delivery.temp_queue_for_delayed_delivery,
        # setting TTL of 300 sec (5 min) for task
        expiration=300,
    )
