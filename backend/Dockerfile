FROM python:3.10
RUN mkdir /usr/src/iwiki-backend/logs /usr/src/iwiki-backend/celery-logs -p
COPY . /usr/src/iwiki-backend
WORKDIR /usr/src/iwiki-backend
RUN pip install -i https://pypi.org/simple/ -r requirements.txt
WORKDIR /usr/src/iwiki-backend
CMD bin/run.sh
