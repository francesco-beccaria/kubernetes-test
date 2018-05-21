.PHONY: build producer consumer beat

build:
	pip install -e .

producer:
	celery -A kubernetes_test.producer.app worker

consumer:
	celery -A kubernetes_test.consumer.app worker

beat:
	celery -A kubernetes_test.producer.app beat
