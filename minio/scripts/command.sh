#!/bin/sh

set -eux

./minio server --address :$API_PORT --console-address :$CONSOLE_PORT $DATA_DIRECTORY