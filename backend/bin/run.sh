#! /bin/sh

python manage.py migrate
nohup celery -A modules.cel worker -l INFO -f /usr/src/iwiki-backend/logs/celery-worker.log > /dev/null 2>&1 &
nohup celery -A modules.cel beat -l INFO -f /usr/src/iwiki-backend/logs/celery-beat.log > /dev/null 2>&1 &
uwsgi --ini /usr/src/iwiki-backend/uwsgi.ini --processes $UWSGI_PROCESSES --threads $UWSGI_THREADS -w wsgi.wsgi:application > /dev/null 2>&1
