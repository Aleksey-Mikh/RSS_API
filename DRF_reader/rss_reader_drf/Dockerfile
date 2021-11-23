FROM python:3.9.7-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app
