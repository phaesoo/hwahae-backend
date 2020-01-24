web: gunicorn hwahae.wsgi --log-file -
migrate: python manage.py migrate --settings=hwahae.settings.production
seed: python manage.py loaddata apps/api/fixtures/*.json --settings=hwahae.settings.production
