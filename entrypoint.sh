#!/bin/sh

python manage.py migrate --noinput

# May raise an error if there is already some data in the database
python manage.py loaddata test_data.json

exec "$@"
