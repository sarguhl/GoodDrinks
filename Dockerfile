FROM ubuntu:20.04

LABEL maintainer="Emil Pehlivan <pehlivanemil@gmail.com>"

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

RUN pip install Flask Pillow requests flask_sqlalchemy pymysql apscheduler

COPY . /app

WORKDIR /app

CMD [ "python3", "./app.py" ]

EXPOSE 5000