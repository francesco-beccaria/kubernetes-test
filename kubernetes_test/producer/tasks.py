import logging
from os import environ
from random import choices
import string

from celery import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@task(bind=True, name='send_message')
def send_message(self):
    num_messages = environ.get('MESSAGES_PER_INTERVAL', 5)

    for i in range(int(num_messages)):
        message = 'This is an outgoing message'
        logger.warning(f'Sending message: {message} ')
        self.app.send_task(
            'receive_message',
            args=(message,),
            exchange='ts.messaging',
            routing_key='message.send'
        )


@task(bind=True, name='receive_response')
def receive_response(self, message):
    logger.warning(f'Received response from consumer: {message}')
