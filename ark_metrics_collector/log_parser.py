# ark_metrics_collector/log_parser.py
import re
import logging
from .metrics import (
    active_players_metric, 
    active_player_count_metric,  # Import the new count metric
    map_name_metric, 
    startup_time_gauge, 
    session_name_metric, 
    cluster_id_metric, 
    cluster_directory_override_metric, 
    installed_mods_metric
)

# Dictionary to track active players
active_players = {}

def parse_log_line(line):
    """Parse a log line and extract metrics based on the log format."""
    logging.debug(f"Parsing line: {line}")

    # Check for player joining
    join_match = re.search(r'(\S+) \[UniqueNetId:(\w+)', line)
    if join_match and "joined this ARK!" in line:
        player_name = join_match.group(1)
        unique_net_id = join_match.group(2)

        # Only set metric if the player is not already logged in
        if unique_net_id not in active_players:
            active_players[unique_net_id] = player_name
            active_players_metric.labels(player_name=player_name).set(1)  # Set active for this player
            active_player_count_metric.inc()  # Increment the total active player count
            logging.debug(f"Player joined: {player_name} with UniqueNetId: {unique_net_id}")
        else:
            logging.debug(f"Player {player_name} with UniqueNetId {unique_net_id} is already logged in.")

    # Check for player leaving
    leave_match = re.search(r'(\S+) \[UniqueNetId:(\w+)', line)
    if leave_match and "left this ARK!" in line:
        player_name = leave_match.group(1)
        unique_net_id = leave_match.group(2)

        # Only unset metric if the player is currently logged in
        if unique_net_id in active_players:
            del active_players[unique_net_id]
            active_players_metric.labels(player_name=player_name).set(0)  # Set inactive for this player
            active_player_count_metric.dec()  # Decrement the total active player count
            logging.debug(f"Player left: {player_name} with UniqueNetId: {unique_net_id}")
        else:
            logging.debug(f"Player {player_name} with UniqueNetId {unique_net_id} is not currently logged in.")



    # Extract map_name
    map_match = re.search(r'Commandline:.*?(\w+_WP)\?', line)
    if map_match:
        map_name = map_match.group(1)
        map_name_metric.labels(map_name=map_name).set(1)
        logging.debug(f"Map name set to: {map_name}")

    # Extract startup time
    startup_match = re.search(r'Full Startup: (\d+\.\d+) seconds', line)
    if startup_match:
        startup_time = float(startup_match.group(1))
        startup_time_gauge.set(startup_time)
        logging.debug(f"Startup time set to: {startup_time}")

    # Extract session_name
    session_name_match = re.search(r'SessionName=([^\?]+)', line)
    if session_name_match:
        session_name = session_name_match.group(1)
        session_name_metric.labels(session_name=session_name).set(1)
        logging.debug(f"Session name set to: {session_name}")

    # Extract cluster_id
    cluster_id_match = re.search(r'-clusterID=(\S+)', line)
    if cluster_id_match:
        cluster_id = cluster_id_match.group(1)
        cluster_id_metric.labels(cluster_id=cluster_id).set(1)
        logging.debug(f"Cluster ID set to: {cluster_id}")

    # Extract cluster_directory_override_path
    cluster_dir_match = re.search(r'-Clusterdiroverride=(\S+)', line)
    if cluster_dir_match:
        cluster_directory = cluster_dir_match.group(1)
        cluster_directory_override_metric.labels(cluster_directory_override=cluster_directory).set(1)
        logging.debug(f"Cluster directory override path set to: {cluster_directory}")

    # Extract installed mods (list of mods, each mod has its own label)
    mods_match = re.search(r'-mods=([\d,]+)', line)
    if mods_match:
        mods = mods_match.group(1).split(',')
        for mod_id in mods:
            installed_mods_metric.labels(mod_id=mod_id).set(1)
            logging.debug(f"Installed mod ID set to: {mod_id}")

