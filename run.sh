#!/bin/bash -e
PIPENV_DONT_LOAD_ENV=1 /usr/bin/python3 -m pipenv run gunicorn -w 2  \
    -b unix:/societies/qjcr/lightbluetent/web.sock \
    --log-level=info \
    --log-file production.log wsgi:app
