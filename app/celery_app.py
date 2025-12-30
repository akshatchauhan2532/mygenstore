from celery import Celery

celery_app = Celery(
    "mygenstore",
    broker="amqp://guest:guest@localhost:5672/",  # RabbitMQ broker
    backend="rpc://",  # optional, for results
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks([
    "app.notifications",
])
