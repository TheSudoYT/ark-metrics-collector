import argparse
import yaml
from .app import start

def main():
    parser = argparse.ArgumentParser(description="Ark Metrics Collector")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to the config file")
    args = parser.parse_args()

    # Pass the config file path to the start function
    start(config_path=args.config)

if __name__ == "__main__":
    main()