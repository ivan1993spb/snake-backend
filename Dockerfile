FROM python:3.8-alpine3.10

ENV PYTHONUNBUFFERED=1 \
    LIBRARY_PATH=/lib:/usr/lib

RUN apk add --no-cache libjpeg

COPY requirements.txt requirements.txt

RUN apk add --virtual deps --no-cache \
    build-base \
    zlib-dev \
    jpeg-dev \
 && pip install -r requirements.txt \
 && apk del deps

WORKDIR /usr/local/app

COPY lib lib
COPY scheduler.py ./
