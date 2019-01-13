FROM ubuntu:16.04

MAINTAINER Atte Jauhiainen "atte.jauhiainen@student.oulu.fi"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev pkg-config \
    libmysqlclient-dev python3-mysqldb


# copy current directory into the container
ADD . /app

# install requirements
RUN pip3 --no-cache-dir install -r /app/requirements.txt

# make port 8000 available to the world outside
EXPOSE 8000

WORKDIR /app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app.server"]