# ark_metrics_collector/app.py
import logging
from flask import Flask, Response
from prometheus_client import generate_latest
import threading
from .polling import poll_log_file

app = Flask(__name__)

# Flask route to expose metrics
@app.route('/metrics')
def metrics():
    """Endpoint to expose metrics for Prometheus scraping."""
    return Response(generate_latest(), mimetype='text/plain')

def start():
    """Start the Flask app and the polling thread."""
    logging.basicConfig(level=logging.DEBUG)

    # Start log polling in a separate thread
    poll_thread = threading.Thread(target=poll_log_file)
    poll_thread.start()

    # Run Flask app for the metrics endpoint
    app.run(host="0.0.0.0", port=5000)