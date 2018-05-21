FROM python:3.6-slim

RUN apt-get update \
    && apt-get -y --no-install-recommends install \
        build-essential \
        curl \
        git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /var/app

WORKDIR /var/app

RUN make build

CMD ["bash"]
