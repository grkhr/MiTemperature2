import os
import json
import datetime
import time
import db
import models

FILENAME = 'data.jsonl'

def stringify_ts(ts):
    if isinstance(ts, int):
        ts = datetime.datetime.fromtimestamp(ts)
    return ts.strftime('%d %b %H:%M')


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def logs_stat():
    ts = time.time()
    with db.session() as sess:
        lines = sess.query(models.MHData.id).count()
    count_time = time.time() - ts

    ts = time.time()
    with db.session() as sess:
        sess.query(models.MHData).order_by(models.MHData.timestamp.desc()).limit(1).first()
    last_line_time = time.time() - ts
    return {
        'lines': lines,
        'count_time': f'{round(1000 * count_time)}ms',
        'last_line_time': f'{round(1000 * last_line_time)}ms'
    }
    # if os.path.exists(FILENAME):
    #     size = os.path.getsize(FILENAME)
    #     size = sizeof_fmt(size)
    #     ts = time.time()
    #     with open(FILENAME) as f:
    #         lines = len(f.readlines())
    #     ts = time.time() - ts
    #     return {
    #         'size': size,
    #         'lines': lines,
    #         'parsing_time': f'{round(1000 * ts)}ms'
    #     }


def find_state(idx):
    with db.session() as sess:
        obj = sess.query(models.MHData).order_by(models.MHData.timestamp.desc()).limit(1).offset(idx).first()
    return obj.__dict__

def find_last_n_states(n):
    with db.session() as sess:
        objs = sess.query(models.MHData).order_by(models.MHData.timestamp.desc()).limit(n).all()
    return [i.__dict__ for i in objs]



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

