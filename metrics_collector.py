import logging
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
import time
import re

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Define Prometheus metrics
map_name_metric = Gauge('ark_map_name_info', 'Current map name on the server', ['map_name'])
startup_time_gauge = Gauge('ark_startup_time_seconds', 'Time taken for full server startup in seconds')
player_count_gauge = Gauge('ark_player_count', 'Number of players currently online')

# Initialize storage for log metrics
log_metrics = {
    "map_name": None,
    "startup_time": None,
    "player_count": 0
}

def parse_log_line(line):
    """Parse a log line and extract metrics based on the log format."""
    logging.debug(f"Parsing line: {line}")

    # Extract map_name and set it as a label
    map_match = re.search(r'Commandline:.*?(\w+_WP)\?', line)
    if map_match:
        log_metrics["map_name"] = map_match.group(1)
        map_name_metric.labels(map_name=log_metrics["map_name"]).set(1)
        logging.debug(f"Map name set to: {log_metrics['map_name']}")

    # Extract startup time if "Full Startup" appears
    startup_match = re.search(r'Full Startup: (\d+\.\d+) seconds', line)
    if startup_match:
        log_metrics["startup_time"] = float(startup_match.group(1))
        startup_time_gauge.set(log_metrics["startup_time"])
        logging.debug(f"Startup time set to: {log_metrics['startup_time']}")

    # Detect server advertisement for player count initialization
    if "Server has completed startup and is now advertising" in line:
        log_metrics["player_count"] = 0
        player_count_gauge.set(log_metrics["player_count"])
        logging.debug("Player count initialized to 0")

def poll_log_file(log_file_path):
    """Polls the log file every 10 seconds and parses new lines."""
    last_position = 0
    while True:
        with open(log_file_path, "r") as f:
            # Move to the last read position
            f.seek(last_position)
            # Read new lines from the file
            lines = f.readlines()
            # Update last position
            last_position = f.tell()

            # Parse each new line
            for line in lines:
                parse_log_line(line)

        # Wait for 10 seconds before polling again
        time.sleep(10)

# Flask route to expose metrics
@app.route('/metrics')
def metrics():
    """Endpoint to expose metrics for Prometheus scraping."""
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    # Start log polling in a separate thread
    import threading
    log_file_path = "/ark-asa/ShooterGame/Saved/Logs/ShooterGame.log"
    poll_thread = threading.Thread(target=poll_log_file, args=(log_file_path,))
    poll_thread.start()

    # Run Flask app for the metrics endpoint
    app.run(host="0.0.0.0", port=5000)