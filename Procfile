release: python manage.py migrate
web: gunicorn ezonseller.wsgi --log-file -
worker: python manage.py celery worker --without-gossip --without-mingle --loglevel=info
beat: python manage.py celery beat --loglevel=info