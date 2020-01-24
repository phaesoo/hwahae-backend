#!/bin/bash

python manage.py makemigrations --settings=hwahae.settings.local
python manage.py migrate --settings=hwahae.settings.local
# load initial data
python manage.py loaddata apps/api/fixtures/*.json --settings=hwahae.settings.local

python manage.py runserver 0.0.0.0:8000 --settings=hwahae.settings.local
