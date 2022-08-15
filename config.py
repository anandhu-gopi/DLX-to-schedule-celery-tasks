"""Config settings."""

from pydantic import BaseSettings


class Config(BaseSettings):
    """Base configuration."""

    # If you create a model that inherits from ,
    # pydantic.BaseSettings the model initialiser
    # will attempt to determine the values of any
    # fields not passed as keyword arguments by
    # reading from the environment.
    RABBITMQ_PROTOCOL: str = "amqp"
    RABBIT_MQ_USERNAME: str = ""
    RABBIT_MQ_PSWD: str = ""
    RABBITMQ_HOST: str = ""
    RABBITMQ_PORT: str = ""
    RABBITMQ_VHOST: str = ""
    RABBITMQ_VHOST_FOR_CELERY: str = ""


config = Config(_env_file=".env")
