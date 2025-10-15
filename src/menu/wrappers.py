"""
wrappers.py - Import facade for menu.wrappers package
This file re-exports all wrapper functions from the wrappers subpackage.

All wrapper functions have been organized into categorized modules:
- wrappers.config: Configuration editing wrappers
- wrappers.hosts: /etc/hosts management wrappers  
- wrappers.server: HTTP server management wrappers
- wrappers.scanning: Scanning operation wrappers
- wrappers.tools: Tool download/management wrappers
- wrappers.utility: Miscellaneous utility wrappers
"""

# Config wrappers
from .wrappers.config import (
    wrap_edit_metadata_field,
    wrap_edit_network_field,
    wrap_edit_credentials_field,
)

# Hosts management wrappers
from .wrappers.hosts import (
    wrap_update_hosts,
    wrap_remove_hosts,
    wrap_view_hosts,
)

# Server management wrappers
from .wrappers.server import (
    wrap_start_server,
    wrap_stop_server,
    wrap_restart_server,
    wrap_server_status,
    wrap_view_server_log,
)

# Scanning wrappers
from .wrappers.scanning import (
    wrap_run_initial_scan,
    wrap_run_full_scan,
    wrap_run_udp_scan,
    wrap_view_scan_results,
)

# Tools management wrappers
from .wrappers.tools import (
    wrap_download_linux_tools,
    wrap_download_windows_tools,
    wrap_download_ad_tools,
    wrap_download_all_tools,
    wrap_list_tools,
    wrap_remove_tools_menu,
)

# Utility wrappers
from .wrappers.utility import (
    wrap_open_notes,
    wrap_open_scans,
    wrap_show_lab_info,
)

__all__ = [
    # Config
    'wrap_edit_metadata_field',
    'wrap_edit_network_field',
    'wrap_edit_credentials_field',
    # Hosts
    'wrap_update_hosts',
    'wrap_remove_hosts',
    'wrap_view_hosts',
    # Server
    'wrap_start_server',
    'wrap_stop_server',
    'wrap_restart_server',
    'wrap_server_status',
    'wrap_view_server_log',
    # Scanning
    'wrap_run_initial_scan',
    'wrap_run_full_scan',
    'wrap_run_udp_scan',
    'wrap_view_scan_results',
    # Tools
    'wrap_download_linux_tools',
    'wrap_download_windows_tools',
    'wrap_download_ad_tools',
    'wrap_download_all_tools',
    'wrap_list_tools',
    'wrap_remove_tools_menu',
    # Utility
    'wrap_open_notes',
    'wrap_open_scans',
    'wrap_show_lab_info',
]