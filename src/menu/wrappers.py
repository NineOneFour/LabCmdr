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

from ..config import Colors
from ..actions import (
    download_lin,
    download_win,
    download_ad,
)

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


def wrap_download_all_tools(config):
    """Download all tools"""
    print(f"\n{Colors.CYAN}[*] Downloading ALL enumeration tools...{Colors.NC}")
    print(f"{Colors.YELLOW}[*] This will download Linux, Windows, and AD tools{Colors.NC}\n")
    
    # Ask if user wants to force re-download



    print(f"{Colors.YELLOW}Overwrite existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'ye'
    
    try:
        print(f"\n{Colors.BLUE}[1/3] Linux Tools{Colors.NC}")
        download_linux_tools(force=force)
        
        print(f"\n{Colors.BLUE}[2/3] Windows Tools{Colors.NC}")
        download_windows_tools(force=force)
        
        print(f"\n{Colors.BLUE}[3/3] Active Directory Tools{Colors.NC}")
        download_ad_tools(force=force)
        
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.GREEN}║     All Tools Downloaded!                ║{Colors.NC}")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════╝{Colors.NC}")
        
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading tools: {e}{Colors.NC}")

def wrap_list_tools(config):
    """List available tools"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Tool Status Overview             ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}")
    
    try:
        # Show all three categories
        list_linux_tools()
        list_windows_tools()
        list_ad_tools()
        
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error listing tools: {e}{Colors.NC}")

def wrap_remove_all_tools(config):
    """Remove all tools"""
    print(f"\n{Colors.RED}[!] WARNING: This will remove ALL tools{Colors.NC}")
    print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
    if input().strip().lower() == 'y':
        total = 0
        total += remove_linux_tools()
        total += remove_windows_tools()
        total += remove_ad_tools()
        print(f"\n{Colors.GREEN}[+] Removed {total} total tools{Colors.NC}")
    else:
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
