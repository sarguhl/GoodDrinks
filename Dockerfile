FROM ubuntu:18.04
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

LABEL maintainer="Emil Pehlivan <pehlivanemil@gmail.com>"

RUN apt-get update -y && apt-get install -y python-pip python-dev

RUN pip install Flask Pillow requests flask_sqlalchemy

COPY . /app

WORKDIR /app

CMD [ "python", "./app.py" ]