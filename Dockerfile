# Start from a Python3.7 base image I published


FROM python:3.9-slim AS mi2

RUN apt-get update && \
	apt-get install gcc build-essential dbus -y && \
	apt-get clean

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
# ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

RUN apt-get -y --no-install-recommends install libglib2.0-dev

#RUN which python
#RUN which pip

COPY . .
# RUN sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.7m 10
#RUN sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.7 10

RUN which python
RUN which pip

RUN python --version
RUN pip --version

RUN pip install bluepy
RUN pip install requests
RUN pip install -r requirements.txt

#COPY LYWSD03MMC.py LYWSD03MMC.py 
#COPY sendtovera.py sendtovera.py 


RUN service dbus start

#Change to the following line to match your needs

# ENTRYPOINT while true; do /usr/local/bin/python3.7m LYWSD03MMC.py -d A4:C1:38:04:2A:02 -r -b 100 --skipidentical 0 -deb --callback sendToFile.sh; sleep 2; done
ENTRYPOINT python run.py
# start the created image with sudo docker run --net=host -t your_image_name /bin/bash
