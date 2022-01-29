FROM python:3.9
RUN mkdir /usr/src/iwiki-backend -p
RUN mkdir /usr/src/iwiki-backend/logs -p
COPY . /usr/src/iwiki-backend
WORKDIR /usr/src/iwiki-backend
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
WORKDIR /usr/src/iwiki-backend
CMD bin/run.sh
