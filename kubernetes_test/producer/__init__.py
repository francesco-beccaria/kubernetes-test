from datetime import timedelta
from os import environ
from random import randint

from kombu import Exchange, Queue, binding

from kubernetes_test.factory.celery import init_celery


def init_producer():

    # GET MESSAGE INTERVAL
    # GET NUM MESSAGES PER INTERVAL

    CONSUMING_ROUTING_KEYS = [
        'message.response'
    ]

    app = init_celery('producer', 'kubernetes_test.producer', CONSUMING_ROUTING_KEYS)

    message_interval = int(environ.get('MESSAGE_INTERVAL', 5))

    app.conf.beat_schedule = {
        'send_message': {
            'task': 'send_message',
            'schedule': timedelta(seconds=message_interval),
            'args': (),
        },
    }

    return app


app = init_producer()
