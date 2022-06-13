from multiprocessing import Process
import os

cmd = [
    'while true; do /usr/local/bin/python3.7m LYWSD03MMC.py -d A4:C1:38:04:2A:02 -r -b 100 --skipidentical 0 -deb --callback sendToFile.sh; sleep 2; done',
    'python checker/bot.py'
]

for c in cmd:
    p = Process(target=os.system, args=(c,))
    p.start()