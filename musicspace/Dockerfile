ARG RUNTIME_VERSION="3.10"
ARG PLATFORM="linux/amd64"
ARG REQUIREMENTS_FILE="requirements.txt"

FROM --platform=$PLATFORM python:${RUNTIME_VERSION}-bullseye AS python-bullseye

ENV PYTHONUNBUFFERED 1

ARG APPLICATION_DIR="/src"

ARG REQUIREMENTS_FILE

RUN apt-get update -y

## if we actually deploy this container, we should remove this
RUN apt-get install -y postgresql-client

RUN python -m pip install -U pip

ADD $REQUIREMENTS_FILE ${APPLICATION_DIR}/requirements.txt
RUN pip install -r ${APPLICATION_DIR}/requirements.txt

ADD . ${APPLICATION_DIR}

WORKDIR ${APPLICATION_DIR}