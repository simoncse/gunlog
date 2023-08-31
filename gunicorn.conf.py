import multiprocessing
import os
from distutils.util import strtobool

max_requests = 1000
max_requests_jitter = 50

bind = os.getenv("WEB_BIND", "0.0.0.0:8000")
backlog = 2048
accesslog = "-"
access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' in %(D)sµs"  # noqa: E501
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2))
worker_class = "uvicorn.workers.UvicornWorker"
logger_class = "backend.http.logger_setup.GunicornLogger"

threads = int(os.getenv("PYTHON_MAX_THREADS", 1))

reload = bool(strtobool(os.getenv("WEB_RELOAD", "false")))


#
# Server Hooks
#
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass
