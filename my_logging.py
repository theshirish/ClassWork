import logging
import json
from datetime import datetime


class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "level": record.levelname,
            "message": record.getMessage()
            # "module": record.module,
            # "function": record.funcName,
            # "line_no": record.lineno
        }
        return json.dumps(log_record)


def setup_logger(name="MyLogger",  level=logging.INFO):
    # handler = logging.FileHandler(log_file)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
