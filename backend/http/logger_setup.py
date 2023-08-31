import logging
import logging.config
import sys

from gunicorn.glogging import Logger
from loguru import logger

##
## Reference and Discussion in Comments
# https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
##


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class GunicornLogger(Logger):
    def setup(self, cfg):
        handler = InterceptHandler()
        self.error_log.addHandler(handler)
        self.error_log.setLevel(logging.INFO)
        self.access_log.addHandler(handler)
        self.access_log.setLevel(logging.INFO)

        # Configure logger before gunicorn starts logging
        logger.configure(handlers=[{"sink": sys.stdout, "level": logging.INFO}])


def configure_logger() -> None:
    intercept_handler = InterceptHandler()
    # logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]


    logger.configure(
        handlers=[
            {"sink": 'log/master.log', "level": logging.INFO},
            {"filter":"backend.features.foo","sink": 'log/foo.log', "level": logging.INFO},
        ]
    )

    logger.add("log/server/gunciorn.log", filter="gunicorn", level="INFO", rotation="00:00", retention="14 days")
    logger.add("log/server/uvicorn.log", filter="uvicorn", level="INFO", rotation="00:00", retention="14 days")