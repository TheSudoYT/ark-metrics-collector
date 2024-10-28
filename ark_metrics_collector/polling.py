# ark_metrics_collector/polling.py
import time
import logging
from .config import config
from .log_parser import parse_log_line

def poll_log_file():
    """Polls the log file at the configured interval and parses new lines."""
    log_file_path = config["log_file_path"]
    poll_interval = config["poll_interval"]
    last_position = 0

    while True:
        with open(log_file_path, "r") as f:
            f.seek(last_position)
            lines = f.readlines()
            last_position = f.tell()

            for line in lines:
                parse_log_line(line)

        time.sleep(poll_interval)
