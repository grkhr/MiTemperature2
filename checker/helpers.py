import os
import json
import datetime

FILENAME = 'data.jsonl'

def find_current_state():
    if os.path.exists(FILENAME):
        with open(FILENAME) as f:
            state = f.readlines()[-1]
        return json.loads(state)

def format_state(state):
    if state is None:
        return 'NONE'
    dtm = datetime.datetime.fromtimestamp(state['timestamp']).strftime('%d %b %H:%M')
    text = [
        f"{dtm} UTC",
        f"{state['temperature']}C - temperature",
        f"{state['humidity']}% - humidity",
    ]
    return '\n'.join(text)
