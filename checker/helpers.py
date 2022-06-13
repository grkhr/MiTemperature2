import os
import json
import datetime
import time

FILENAME = 'data.jsonl'

def stringify_ts(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%d %b %H:%M')


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def logs_stat():
    if os.path.exists(FILENAME):
        size = os.path.getsize(FILENAME)
        size = sizeof_fmt(size)
        ts = time.time()
        with open(FILENAME) as f:
            lines = len(f.readlines())
        ts = time.time() - ts
        return {
            'size': size,
            'lines': lines,
            'parsing_time': f'{round(1000 * ts)}ms'
        }


def find_state(idx):
    if os.path.exists(FILENAME):
        with open(FILENAME) as f:
            state = f.readlines()[idx]
        return json.loads(state)

def find_last_n_states(n):
    if os.path.exists(FILENAME):
        with open(FILENAME) as f:
            states = f.readlines()[-n:]
        return [json.loads(i) for i in states]



def format_state(state):
    if state is None:
        return 'NONE'
    dtm = stringify_ts(state['timestamp'])
    text = [
        f"{dtm} UTC",
        f"{state['temperature']}°C - temperature",
        f"{state['humidity']}% - humidity",
    ]
    return '\n'.join(text)

def sort_config(config):
    return dict(sorted(config.items(), key=lambda x: x[1]['sort']))

