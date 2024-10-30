# ark_metrics_collector/app.py
import logging
from flask import Flask, Response
from prometheus_client import generate_latest
import threading
from .polling import poll_log_file
from .config import load_config

app = Flask(__name__)

# Flask route to expose metrics
@app.route('/metrics')
def metrics():
    """Endpoint to expose metrics for Prometheus scraping."""
    return Response(generate_latest(), mimetype='text/plain')

def start(config_path):
    """Start the Flask app and the polling thread."""
    metrics_collector_port = config["metrics_collector_port"]
    config = load_config(config_path)

    print(f"Poll interval: {config['poll_interval']}")
    print(f"Log file path: {config['log_file_path']}")
    print(f"Metrics collector port: {config['metrics_collector_port']}")

    logging.basicConfig(level=logging.DEBUG)

    # Start log polling in a separate thread
    poll_thread = threading.Thread(target=poll_log_file)
    poll_thread.start()

    # Run Flask app for the metrics endpoint
    app.run(host="0.0.0.0", port=metrics_collector_port)
