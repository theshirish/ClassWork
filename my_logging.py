import logging
import json
from datetime import datetime
from venv import logger
from xml.sax import handler


class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).strftime('%Y-%m-%d#%H:%M:%S.%f')[:-3],
            "level": record.levelname,
            "message": record.getMessage()
            # "module": record.module,
            # "function": record.funcName,
            # "line_no": record.lineno
        }
        return json.dumps(log_record)


def setup_logger(name="MyLogger",  level=logging.INFO):
    # handler_f = logging.FileHandler("service.log")
    # handler_f.setFormatter(CustomJsonFormatter())

    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())

    logger = logging.getLogger(name)
    logger.setLevel(level)
    # logger.addHandler(handler_f)
    logger.addHandler(handler)

    return logger
