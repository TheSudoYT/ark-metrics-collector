import time
import logging
from .log_parser import parse_log_line

def poll_log_file(log_file_path, poll_interval):
    """Polls the log file at the specified interval and parses new lines."""
    last_position = 0

    while True:
        with open(log_file_path, "r") as f:
            f.seek(last_position)
            lines = f.readlines()
            last_position = f.tell()

            for line in lines:
                parse_log_line(line)

        time.sleep(poll_interval)

