web: gunicorn hwahae.wsgi --log-file -
migrate: python manage.py migrate --settings=hwahae.settings.production
seed: python manage.py loaddata api/fixtures/ingredient.json --settings=hwahae.settings.production
seed: python manage.py api/fixtures/item.json --settings=hwahae.settings.production