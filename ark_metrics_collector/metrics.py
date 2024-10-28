# ark_metrics_collector/metrics.py
from prometheus_client import Gauge

map_name_metric = Gauge('ark_map_name_info', 'Current map name on the server', ['map_name'])
startup_time_gauge = Gauge('ark_startup_time_seconds', 'Time taken for full server startup in seconds')
session_name_metric = Gauge('ark_session_name_info', 'Current session name of the server', ['session_name'])
cluster_id_metric = Gauge('ark_cluster_id_info', 'Cluster ID associated with the server', ['cluster_id'])
cluster_directory_override_metric = Gauge('ark_cluster_directory_override', 'Cluster directory override path', ['cluster_directory_override'])
installed_mods_metric = Gauge('ark_installed_mods_info', 'Installed mods on the server', ['mod_id'])
active_players_metric = Gauge('ark_active_players', 'Players currently logged into the Ark', ['player_name'])
active_player_count_metric = Gauge('ark_active_player_count', 'Total number of players currently logged into the Ark')
