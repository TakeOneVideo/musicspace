#!/bin/sh

set -eux

python /src/manage.py migrate
python /src/manage.py createsuperuser --noinput || true
python /src/manage.py collectstatic --noinput || true

exec "$@"