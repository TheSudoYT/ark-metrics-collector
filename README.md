# ark-metrics-collector
Prometheus metrics exporter service for Ark Survival Ascended servers.

## Grafana Dashboard

Grafana dashboard provided for use https://grafana.com/grafana/dashboards/22189-ark-survival-ascended/

## Installing (pip)

1. Install python3-pip
2. Run `pip install ark-metrics-collector`
3. Create a `config.yaml` with the [Ark Metrics Collector Configuration](#ark-metrics-collector-configuration) 
4. Run `ark-metrics-collector --config=/path/to/config.yaml`

## Installing (Docker)

A `config.yaml` with the [Ark Metrics Collector Configuration](#ark-metrics-collector-configuration) is required to be mounted at `/app/config.yaml` within the container. Port 5000 is exposed. Ensure the port mapping to 5000 matches the port defined in the `config.yaml` file. Mount  the `ShooterGame.log` somewhere in the container that matches the `log_file_path` set in `config.yaml`.

```bash
docker run -d -p 5000:5000 --name ark-metrics-collector \
-v /opt/config.yaml:/app/config.yaml \
-v /ark-asa/ShooterGame/Saved/Logs/ShooterGame.log:/app/ShooterGame.log \
ark-metrics-collector
```

## Requirements

You must have:

- Grafana alloy or another metrics scrapping tool capable of scraping prometheus metrics.
- A Promtheus server to forward metrics to.
- Python3 installed.

The following arguments are required when starting Ark to display all possible metrics:

`-servergamelog -servergamelogincludetribelogs -ServerRCONOutputTribeLogs`

## Ark Metrics Collector Configuration

Modify `config.yaml`. The following are configuration options:

| Key                   | Description                              | Example Value                          |
|-----------------------|------------------------------------------|----------------------------------------|
| `poll_interval`       | Polling interval in seconds              | `10`                                   |
| `log_file_path`       | Path to the Ark log file. For container deployments, set to a path inside the container that is mounted to ShooterGame.log. | `"/path/to/ShooterGame/Saved/Logs/ShooterGame.log"` |
| `metrics_collector_port` | Port to expose `/metrics` endpoint. For container deployments set to 5000 until support for custom ports in containers is added.     | `5001`                                 |

Example:

```yaml
poll_interval: 10                                                 
log_file_path: "/ark-asa/ShooterGame/Saved/Logs/ShooterGame.log"  
metrics_collector_port: 5002                                      
```

## Grafana Alloy Configuration

- Ensure `host` is set to the fully qualified domain name (FQDN) of the host. 
- `__address__` is the address of the server running the ark-metrics-collector. Leave as `localhost:<port>` if alloy is running on the same host as ark-metrics-collector.
- Ensure `endpoint url` is set to the address of the prometheus server.

```alloy
prometheus.scrape "scrape_ark" {
  targets = [
    {"__address__" = "localhost:5000", "host" = "ark-scorched-earth.lab.com"},
  ]

  metrics_path = "/metrics"

  forward_to      = [prometheus.remote_write.metrics_service.receiver]
  scrape_interval = "10s"
}

prometheus.scrape "scrape_metrics" {
  targets         = prometheus.exporter.unix.local_system.targets
  forward_to      = [prometheus.remote_write.metrics_service.receiver]
  scrape_interval = "10s"
}

prometheus.remote_write "metrics_service" {
    endpoint {
        url = "http://monitor.lab.com:9090/api/v1/write"

        // basic_auth {
        //   username = "admin"
        //   password = "admin"
        // }
    }
}
```