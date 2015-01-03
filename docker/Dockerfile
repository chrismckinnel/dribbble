FROM ubuntu:14.04
MAINTAINER Chris McKinnel <chrismckinnel@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq              && \
    apt-get dist-upgrade -y         && \
    apt-get install -y build-essential \
                       python-dev      \
                       python-pip      \
                       memcached    && \
    apt-get clean                   && \
    apt-get autoclean

RUN apt-get install -y libssl-dev
RUN apt-get install -y libffi-dev

ADD docker/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD dribbble /var/www

CMD /var/www/runserver.py

EXPOSE 5000