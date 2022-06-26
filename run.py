from multiprocessing import Process
import os

cmd = [
    'while true; do python LYWSD03MMC.py -d A4:C1:38:04:2A:02 -r -b 100 --skipidentical 0 -deb --callback checker/check_data.py --json; sleep 2; done',
    # 'while true; do python LYWSD03MMC.py -d A4:C1:38:D2:ED:D7 -r -b 100 --skipidentical 0 -deb --callback checker/check_data.py --json; sleep 2; done',
    'python checker/bot.py'
]

for c in cmd:
    p = Process(target=os.system, args=(c,))
    p.start()



