ARG RUNTIME_VERSION="3.10"
ARG APPLICATION_DIR="/src"
ARG PLATFORM="linux/amd64"
ARG REQUIREMENTS_FILE="/requirements.txt"
ARG LICENSE_INFO_FILE="/license_info.csv"

FROM --platform=$PLATFORM python:${RUNTIME_VERSION}-bullseye AS build-stage

RUN apt-get update -y

RUN python -m pip install -U pip

COPY requirements.dev.txt .

RUN pip3 install -r requirements.dev.txt

RUN bash -c "echo \"#This was auto-generated on `date` by update_dependencies.sh. DO NOT MANUALLY CHANGE THIS FILE.\";echo;pip3 freeze" > /tmp/requirements.txt

RUN pip3 install -U pip-licenses
RUN bash -c "pip-licenses --with-urls --format=csv" > /tmp/license_info.csv

# Generate a filesystem image with just the requirements file as the output.
# See: https://docs.docker.com/engine/reference/commandline/build/#custom-build-outputs
FROM scratch AS export-stage

ARG REQUIREMENTS_FILE
ARG LICENSE_INFO_FILE

COPY --from=build-stage /tmp/requirements.txt $REQUIREMENTS_FILE
COPY --from=build-stage /tmp/license_info.csv $LICENSE_INFO_FILE