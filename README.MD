# Using DLX (dead-letter-exchange) to schedule celery tasks.

## Description
We will [DLX](https://www.rabbitmq.com/dlx.html) to schedule celery tasks


## Getting started

1. Make sure you have Python 3.7+ installed.
2. Make sure that you have a Rabbitmq server installed and available.


## For Installation of Python Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

## Required Configs

```python
RABBITMQ_PROTOCOL: str = ""
RABBIT_MQ_USERNAME: str = ""
RABBIT_MQ_PSWD: str = ""
RABBITMQ_HOST: str = ""
RABBITMQ_PORT: str = ""
RABBITMQ_VHOST: str = ""
RABBITMQ_VHOST_FOR_CELERY: str = ""
```
### Optional 
You can create a file named .env in the project root folder and add the above values.

# How to run

## run command for main app

```bash
python3 __main__.py
```

## run command for celery worker

```bash
celery -A  celery_app  worker -l  info -Q add-tasks  -c 1
```