# Start from a Python3.7 base image I published

FROM xavierrrr/xrrzero:stretchpython3.7 as mi2

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
# ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

RUN sudo apt-get update

RUN sudo apt-get -y --no-install-recommends install python-pip libglib2.0-dev

COPY . .

RUN /usr/local/bin/pip3.7 install bluepy
RUN /usr/local/bin/pip3.7 install requests
RUN pip install -r requirements.txt

#COPY LYWSD03MMC.py LYWSD03MMC.py 
#COPY sendtovera.py sendtovera.py 


RUN service dbus start

#Change to the following line to match your needs

# ENTRYPOINT while true; do /usr/local/bin/python3.7m LYWSD03MMC.py -d A4:C1:38:04:2A:02 -r -b 100 --skipidentical 0 -deb --callback sendToFile.sh; sleep 2; done
ENTRYPOINT python run.py
# start the created image with sudo docker run --net=host -t your_image_name /bin/bash
