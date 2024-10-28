# ark_metrics_collector/config.py
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

config = load_config()
