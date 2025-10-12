#!/usr/bin/env python3
"""
server.py - Server management actions
High-level functions for managing HTTP server lifecycle
"""

import os
import sys
import signal
import atexit
import threading
import subprocess
from datetime import datetime
from pathlib import Path

from ..config import Colors
from ..core.context import load_lab_config, save_lab_config, find_lab_root
from ..core.http_server import start_server, check_port_available, get_tun0_ip


# Global state
_server_instance = None
_server_thread = None
_log_file_path = None


def start_lab_server(port=8080):
    """
    Start HTTP server in background thread.
    Handles port conflicts automatically.
    
    Args:
        port: Desired port number (will increment if in use)
    
    Returns:
        bool: True if started successfully, False otherwise
    """
    global _server_instance, _server_thread, _log_file_path
    
    # Check if server already running
    if is_server_running():
        print(f"{Colors.YELLOW}[!] Server is already running{Colors.NC}")
        status = get_server_status()
        print(f"{Colors.CYAN}[*] Running on port {status['port']}{Colors.NC}")
        return False
    
    # Find available port
    original_port = port
    while not check_port_available(port):
        print(f"{Colors.YELLOW}[!] Port {port} is in use, trying {port + 1}...{Colors.NC}")
        port += 1
        
        # Safety check - don't try forever
        if port > original_port + 100:
            print(f"{Colors.RED}[!] Could not find available port{Colors.NC}")
            return False
    
    if port != original_port:
        print(f"{Colors.GREEN}[+] Using port {port}{Colors.NC}\n")
    
    # Get lab root and log path
    lab_root = find_lab_root()
    _log_file_path = lab_root / "labcmdr" / "httpserver.log"
    
    try:
        # Start the server
        print(f"{Colors.CYAN}[*] Starting HTTP server...{Colors.NC}\n")
        httpd = start_server(port)
        
        if not httpd:
            print(f"{Colors.RED}[!] Failed to start server{Colors.NC}")
            return False
        
        # Store server instance
        _server_instance = httpd
        
        # Start server in background thread
        _server_thread = threading.Thread(
            target=httpd.serve_forever,
            daemon=True,
            name="LabHttpServer"
        )
        _server_thread.start()
        
        # Get server details
        pid = os.getpid()
        ip = get_tun0_ip()
        started_at = datetime.now().isoformat()
        
        # Update config
        config = load_lab_config()
        if 'runtime' not in config:
            config['runtime'] = {}
        
        config['runtime']['server_running'] = True
        config['runtime']['server_port'] = port
        config['runtime']['server_pid'] = pid
        config['runtime']['server_started_at'] = started_at
        config['runtime']['server_log'] = str(_log_file_path)
        config['runtime']['server_ip'] = ip
        
        save_lab_config(config)
        
        # Register cleanup handlers
        _register_cleanup_handlers()
        
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.GREEN}║     Server Started Successfully!         ║{Colors.NC}")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════╝{Colors.NC}\n")
        
        print(f"{Colors.CYAN}Server running in background{Colors.NC}")
        print(f"{Colors.CYAN}Use 'Stop Server' menu option to shut down{Colors.NC}\n")
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error starting server: {e}{Colors.NC}")
        _server_instance = None
        _server_thread = None
        return False


def stop_lab_server():
    """
    Stop running HTTP server.
    
    Returns:
        bool: True if stopped successfully, False otherwise
    """
    global _server_instance, _server_thread
    
    if not is_server_running():
        print(f"{Colors.YELLOW}[!] No server is currently running{Colors.NC}")
        return False
    
    try:
        print(f"{Colors.CYAN}[*] Stopping HTTP server...{Colors.NC}")
        
        # Shutdown the server
        _server_instance.shutdown()
        
        # Wait for thread to finish (with timeout)
        if _server_thread:
            _server_thread.join(timeout=5)
        
        # Clear global state
        _server_instance = None
        _server_thread = None
        
        # Update config
        config = load_lab_config()
        if 'runtime' in config:
            config['runtime']['server_running'] = False
            config['runtime']['server_port'] = None
            config['runtime']['server_pid'] = None
            config['runtime']['server_started_at'] = None
            config['runtime']['server_log'] = None
            config['runtime']['server_ip'] = None
        
        save_lab_config(config)
        
        print(f"{Colors.GREEN}[+] Server stopped successfully{Colors.NC}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error stopping server: {e}{Colors.NC}")
        return False


def restart_lab_server(port=None):
    """
    Restart HTTP server with same or different port.
    
    Args:
        port: New port (None = use current port)
    
    Returns:
        bool: True if restarted successfully
    """
    # Get current port if not specified
    if port is None:
        status = get_server_status()
        port = status.get('port', 8080)
    
    print(f"{Colors.CYAN}[*] Restarting server on port {port}...{Colors.NC}\n")
    
    # Stop current server
    if is_server_running():
        if not stop_lab_server():
            return False
        print()
    
    # Start new server
    return start_lab_server(port)


def _register_cleanup_handlers():
    """Register cleanup handlers for graceful shutdown"""
    # Register atexit handler
    atexit.register(cleanup_server_on_exit)
    
    # Register signal handlers (only if not already registered)
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    except:
        # Signals might already be registered or not available
        pass


def cleanup_server_on_exit():
    """Cleanup function called on normal exit"""
    if is_server_running():
        print(f"\n{Colors.YELLOW}[*] Cleaning up server...{Colors.NC}")
        stop_lab_server()


def signal_handler(sig, frame):
    """Handle interrupt signals (Ctrl+C, SIGTERM)"""
    print(f"\n{Colors.YELLOW}[*] Received signal {sig}, shutting down...{Colors.NC}")
    cleanup_server_on_exit()
    sys.exit(0)


def get_server_status():
    """
    Get current server status and information.
    
    Returns:
        dict: Server status information
    """
    config = load_lab_config()
    runtime = config.get('runtime', {})
    
    is_running = _server_instance is not None
    port = runtime.get('server_port')
    pid = runtime.get('server_pid')
    started_at = runtime.get('server_started_at')
    log_file = runtime.get('server_log')
    ip = runtime.get('server_ip')
    
    # Calculate uptime if running
    uptime = None
    if is_running and started_at:
        try:
            start_time = datetime.fromisoformat(started_at)
            uptime = datetime.now() - start_time
        except:
            pass
    
    return {
        'is_running': is_running,
        'port': port,
        'ip': ip,
        'pid': pid,
        'started_at': started_at,
        'uptime': uptime,
        'log_file': log_file
    }


def is_server_running():
    """
    Check if server is currently running.
    
    Returns:
        bool: True if running, False otherwise
    """
    return _server_instance is not None


def view_server_log(live=False):
    """
    View server log file.
    
    Args:
        live: If True, tail -f the log (live view). If False, show last 50 lines.
    """
    log_path = get_log_file_path()
    
    if not log_path or not log_path.exists():
        print(f"{Colors.YELLOW}[!] Log file not found: {log_path}{Colors.NC}")
        return
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Server Log                       ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    try:
        if live:
            print(f"{Colors.YELLOW}[*] Showing live log (Press Ctrl+C to stop)...{Colors.NC}\n")
            subprocess.run(['tail', '-f', str(log_path)])
        else:
            print(f"{Colors.YELLOW}[*] Last 50 lines:{Colors.NC}\n")
            result = subprocess.run(
                ['tail', '-n', '50', str(log_path)],
                capture_output=True,
                text=True
            )
            print(result.stdout)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Stopped viewing log{Colors.NC}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error viewing log: {e}{Colors.NC}")


def get_log_file_path():
    """
    Get path to server log file.
    
    Returns:
        Path: Path to httpserver.log
    """
    try:
        lab_root = find_lab_root()
        return lab_root / "labcmdr" / "httpserver.log"
    except:
        return None