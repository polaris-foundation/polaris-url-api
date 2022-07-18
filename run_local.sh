#!/bin/bash
SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=dhos-url-api
export DATABASE_PASSWORD=dhos-url-api
export DATABASE_NAME=dhos-url-api
export FLASK_APP=dhos_url_api/autoapp.py
export ENVIRONMENT=DEVELOPMENT
export ALLOW_DROP_DATA=true
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}

if [ -z "$*" ]
then
  flask db upgrade
  python3 -m dhos_url_api
else
  python3 -m flask $*
fi
