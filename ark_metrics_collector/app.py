import logging
from flask import Flask, Response
from prometheus_client import generate_latest
import threading
from .config import load_config
from .polling import poll_log_file

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

def start(config_path):
    config = load_config(config_path)

    print(f"Poll interval: {config['poll_interval']}")
    print(f"Log file path: {config['log_file_path']}")
    print(f"Metrics collector port: {config['metrics_collector_port']}")

    logging.basicConfig(level=logging.DEBUG)

    # Start log polling in a separate thread with config values
    poll_thread = threading.Thread(
        target=poll_log_file,
        args=(config['log_file_path'], config['poll_interval'])
    )
    poll_thread.start()

    app.run(host="0.0.0.0", port=config["metrics_collector_port"])

