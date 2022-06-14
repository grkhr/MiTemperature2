FROM python:3.9-slim AS mi2

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
	apt-get install gcc build-essential dbus -y && \
	apt-get clean

RUN apt-get -y --no-install-recommends install libglib2.0-dev

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app

RUN python --version
RUN pip --version

RUN service dbus start
RUN pwd

ENTRYPOINT cd /app && python run.py
