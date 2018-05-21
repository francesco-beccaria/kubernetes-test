from kubernetes_test.factory.celery import init_celery


def init_consumer():
    CONSUMING_ROUTING_KEYS = [
        'message.send'
    ]

    return init_celery('consumer', 'kubernetes_test.consumer', CONSUMING_ROUTING_KEYS)


app = init_consumer()
