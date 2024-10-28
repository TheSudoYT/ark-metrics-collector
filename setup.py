# setup.py
from setuptools import setup, find_packages

setup(
    name="ark_metrics_collector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "prometheus_client",
        "pyyaml"
    ],
    entry_points={
        'console_scripts': [
            'ark-metrics-collector=ark_metrics_collector.app:start'
        ],
    },
)

