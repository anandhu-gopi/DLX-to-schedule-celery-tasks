"""Module contains celery task."""

from celery_app import app


@app.task(
    name="add",
    ignore_result=True,
    acks_late=True,
)
def add(a: int, b: int):
    print(f"{a} + {b} is {a+b}")
