FROM python:3.6-alpine

WORKDIR /app

COPY . /app

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

ENV http_proxy host:5000
ENV https_proxy host:5000

EXPOSE 5000

CMD python manage.py runserver
