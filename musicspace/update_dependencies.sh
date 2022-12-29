#!/usr/bin/env bash
# set -o allexport
# [[ -f ../.env ]] && source ../.env
# set +o allexport

DOCKER_BUILDKIT=1 docker build --build-arg PLATFORM=linux/arm64/v8 --build-arg REQUIREMENTS_FILE=/requirements.arm64.txt --build-arg LICENSE_INFO_FILE=/license_info.arm64.csv --no-cache -o . -f update-dependencies.dockerfile .
DOCKER_BUILDKIT=1 docker build --build-arg PLATFORM=linux/amd64 --build-arg REQUIREMENTS_FILE=/requirements.txt --build-arg LICENSE_INFO_FILE=/license_info.csv --no-cache -o . -f update-dependencies.dockerfile .