ARG PLATFORM="linux/amd64"
ARG SUITE="bullseye"
ARG APPLICATION_DIR="/etc/minio"

FROM --platform=$PLATFORM debian:${SUITE}-slim AS debian-base-image

RUN apt-get update -y

RUN apt-get install -y wget

ARG APPLICATION_DIR

ENV API_PORT="8080"

ENV CONSOLE_PORT="8081"

ENV DATA_DIRECTORY="/var/minio/data"

RUN mkdir ${APPLICATION_DIR}

RUN cd ${APPLICATION_DIR}

RUN pwd

RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio

RUN cp minio ${APPLICATION_DIR}/minio

RUN chmod +x ${APPLICATION_DIR}/minio

RUN ls ${APPLICATION_DIR}

WORKDIR ${APPLICATION_DIR}