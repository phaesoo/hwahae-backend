#!/bin/bash

export MYSQL_ROOT_HOST='127.0.0.1'
export MYSQL_USER='root'
export MYSQL_ROOT_PASSWORD='password'
export MYSQL_DATABASE='my_database'

python manage.py makemigrations --settings=hwahae.settings.local
python manage.py migrate --settings=hwahae.settings.local
# load initial data
python manage.py loaddata api/fixtures/item.json --settings=hwahae.settings.local
python manage.py loaddata api/fixtures/ingredient.json --settings=hwahae.settings.local

python manage.py runserver 0.0.0.0:8000 --settings=hwahae.settings.local
