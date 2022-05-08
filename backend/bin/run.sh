#! /bin/sh

python manage.py migrate
nohup celery -A modules.cel worker -l INFO -f /usr/src/iwiki-backend/celery-logs/worker.log > /dev/null 2>&1 &
nohup celery -A modules.cel beat -l INFO -f /usr/src/iwiki-backend/celery-logs/beat.log > /dev/null 2>&1 &
uwsgi \
--http :8014 \
--processes $UWSGI_PROCESSES \
--threads $UWSGI_THREADS \
--module entry.wsgi \
--logto /usr/src/iwiki-backend/logs/uwsgi.log \
--static-map /static=/usr/src/iwiki-backend/static \
--log-maxsize 10000000
> /dev/null 2>&1
