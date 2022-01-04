FROM ubuntu:20.04

LABEL maintainer="Emil Pehlivan <pehlivanemil@gmail.com>"

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

RUN pip install Flask Pillow requests flask_sqlalchemy

COPY . /app

WORKDIR /app

CMD [ "python", "./app.py" ]

