import argparse
import yaml
from .app import start

def main():
    parser = argparse.ArgumentParser(description="Ark Metrics Collector")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to the config file")
    args = parser.parse_args()

    # Load the configuration
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    print(f"Poll interval: {config['poll_interval']}")
    print(f"Log file path: {config['log_file_path']}")
    print(f"Metrics collector port: {config['metrics_collector_port']}")
    
    # Start the app with the config settings

    start()

if __name__ == "__main__":
    main()