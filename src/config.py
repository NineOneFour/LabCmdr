"""
config.py - Updated LAB_CONFIG with runtime section
Replace the existing LAB_CONFIG in src/config.py with this version
"""

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # No Color


LAB_CONFIG = {
    "metadata": {
        "name": "",                    # machine_name, lab_name, or challenge_name
        "platform": "",                # platform or custom_platform value
        "type": "",                    # from config section of decision tree
        "created": "",                 # datetime when created
        "season": None,                # HTB season number
        "week": None,                  # HTB week number
        "conference": "",              # bsides, defcon, or other
        "conference_name": "",         # when conference is "other"
        "village": "",                 # DefCon village
        "location": "",                # BSides location
        "year": None,                  # Conference year
        "challenge_name": "",          # Conference challenge name
        "category": ""                 # Custom lab category
    },
    "network": {
        "ip_address": None,            # Collected during setup if provided
        "domain": "",
        "domain_name": "",
        "domain_controller": "",
        "fqdn": []
    },
    "credentials": {
        "username": "",                # Collected if has_credentials = yes
        "password": ""                 # Collected if has_credentials = yes
    },
    "runtime": {
        "server_running": False,       # Is HTTP server currently running
        "server_port": None,           # Port server is running on
        "server_pid": None,            # Process ID of server
        "server_started_at": None,     # ISO timestamp when server started
        "server_log": None,            # Path to server log file
        "server_ip": None,             # IP address server is bound to
        "last_scan": None,             # Type of last scan run
        "last_scan_time": None         # When last scan was run
    }
}