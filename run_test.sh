#!/bin/bash

export MYSQL_ROOT_HOST='127.0.0.1'
export MYSQL_USER='root'
export MYSQL_ROOT_PASSWORD='password'
export MYSQL_DATABASE='my_database'

python manage.py test --settings=hwahae.settings.local
