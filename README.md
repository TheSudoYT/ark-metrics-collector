# ark-metrics-collector
Prometheus metrics exporter service for Ark Survival Ascended servers.

## Grafana Dashboard

Grafana dashboard provided for use https://grafana.com/grafana/dashboards/22189-ark-survival-ascended/

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
| `log_file_path`       | Path to the Ark log file                 | `"/path/to/ShooterGame/Saved/Logs/ShooterGame.log"` |
| `metrics_collector_port` | Port to expose `/metrics` endpoint     | `5001`                                 |


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