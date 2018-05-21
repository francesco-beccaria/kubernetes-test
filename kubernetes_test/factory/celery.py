from os import environ

from celery import Celery
from kombu import Exchange, Queue, binding


def init_celery(name, tasks_pkg, routing_keys):
    """
    Initializing celery to point to a rabbitmq type of broker

    Args:
        name (str): Name for the app. Will also be used as the default queue name.
        Will be one of ['consumer', 'producer']
        tasks_pkg (str): Package where tasks for the app being created are located.
            will be either kubernetes_test.producer or kubernetes_test.consumer
        routing_keys (list): List of routing keys to listen on for messages.

    Returns:
        Celery: Celery app object
    """

    # Create celery app
    app = Celery(
        'kubernetes_test.{}'.format(name),
        broker=environ['BROKER_CNX_STRING']
    )

    # Discover tasks appropriate to tge app being created
    app.autodiscover_tasks([tasks_pkg], force=True)

    # Set the default queue name so it matches the app name for easy identification
    app.conf.task_default_queue = name

    # use ts.messaging exchange
    messaging_exchange = Exchange('ts.messaging')

    # add the default queue name to the routing keys list
    routing_keys.append(app.conf.task_default_queue)

    bindings = (
        binding(messaging_exchange, routing_key=routing_key)
        for routing_key in routing_keys
    )

    app.conf.task_queues = [
        Queue(name, list(bindings))
    ]

    return app
