import logging

from celery import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@task(bind=True, name='receive_message')
def receive_message(self, message):
    logger.info('Received {}'.format(message))
    self.app.send_task(
        'receive_response',
        (f'Response to: {message}',),
        exchange='ts.messaging',
        routing_key='message.response'
    )
