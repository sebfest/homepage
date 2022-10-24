#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@example.org \
        --preserve
python manage.py populate_blog
python manage.py collectstatic --no-input --clear
python manage.py runserver 0.0.0.0:8000

exec "$@"
