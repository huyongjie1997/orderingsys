import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import multiprocessing


# bind ip and port
from orderingsys.settings import BASE_DIR

bind = '0.0.0.0:8000'
# The maximum number of pending connections. [2048]
backlog = 512
# work directory
chdir = '/code'
# chdir = '/Users/pointone/Documents/ws'
# timeout
timeout = 30
# Timeout for graceful workers restart. [30]
graceful_timeout = 10

# model: default sync, we use gevent
worker_class = 'gevent'
# process / worker num
workers = multiprocessing.cpu_count() * 2 + 1
# thread num of per process / worker
threads = 2

worker_connections = 1000

# access log format
access_log_format = '%(t)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# access log path
accesslog = '/code/logs/gunicorn/gunicorn.access.log'

# error log level, access log cannot set level
loglevel = 'info'

pidfile = './logs/.gunicorn.pid'
# daemon = True

BASE_LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(BASE_LOG_DIR, exist_ok=True)
os.makedirs(BASE_LOG_DIR + '/gunicorn', exist_ok=True)

