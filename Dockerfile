
FROM ubuntu:18.04

LABEL maintainer="Emil Pehlivan <pehlivanemil@gmail.com>"

RUN apt-get update -y && apt-get install -y python-pip python-dev

RUN pip install Flask Pillow requests

COPY . /app

WORKDIR /app

CMD [ "python", "./app.py" ]