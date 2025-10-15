"""
context.py - Context rendering and header display
Handles dynamic context blocks and headers for menu system
"""

from ..config import Colors
from ..core.http_server import get_interface_ip


def get_attacker_ip(config):
    """Get attacker IP from interface with color"""
    ip = get_interface_ip()
    
    if ip:
        return ip, Colors.GREEN
    else:
        return "VPN Not connected", Colors.RED

def render_context(context_block, config):
    """
    Render a context block with dynamic fields.
    
    Args:
        context_block: Dict with 'title' and 'fields' keys
        config: Lab configuration dictionary
    """
    if not context_block:
        return
    
    title = context_block.get('title', '')
    if title:
        print(f"\n{title}")
    
    fields = context_block.get("fields", [])
    for label, val in fields:
        if callable(val):
            value, color = val(config)
        else:
            value, color = val
        print(f"  {label:<12}: {color}{value}{Colors.NC}")


def main_header(config, title):
    """
    Render the main header box for top-level menu.
    
    Args:
        config: Lab configuration dictionary
        title: Title text to display
    """
    inner_width = 40
    text = f"LabCmdr - {title}"
    padded = text.center(inner_width)
    print(f"{Colors.BLUE}╔{'═' * (inner_width + 2)}╗{Colors.NC}")
    print(f"{Colors.BLUE}║ {padded} ║{Colors.NC}")
    print(f"{Colors.BLUE}╚{'═' * (inner_width + 2)}╝{Colors.NC}")


def submenu_header(config, title):
    """
    Render a simpler header for submenus.
    
    Args:
        config: Lab configuration dictionary
        title: Title text to display
    """
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║ {title:<41}║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}")


# ======================
#   CONTEXT FIELD GETTERS
# ======================

def get_lab_name(config):
    """Get lab name with color"""
    name = (config['metadata'].get('name') or 
            config['metadata'].get('machine_name') or 
            config['metadata'].get('lab_name') or 
            'Unknown Lab')
    return name, Colors.YELLOW


def get_target_ip(config):
    """Get target IP with color"""
    ip = config['network'].get('ip_address', 'Not set')
    return ip, Colors.YELLOW


def get_server_status(config):
    """Get server status with color"""
    runtime = config.get('runtime', {})
    is_running = runtime.get('server_running', False)
    
    if is_running:
        port = runtime.get('server_port', 8080)
        return f"● Running on :{port}", Colors.GREEN
    else:
        return "○ Stopped", Colors.RED


def get_last_scan(config):
    """Get last scan time with color"""
    runtime = config.get('runtime', {})
    last_scan = runtime.get('last_scan')
    
    if last_scan:
        return last_scan, Colors.YELLOW
    else:
        return "Never", Colors.YELLOW


def get_platform(config):
    """Get platform with color"""
    platform = config['metadata'].get('platform', 'Unknown')
    return platform, Colors.YELLOW


def get_fqdn_count(config):
    """Get FQDN count with color"""
    fqdns = config['network'].get('fqdn', [])
    count = len(fqdns)
    
    if count == 0:
        return "None configured", Colors.RED
    elif count == 1:
        return f"{fqdns[0]}", Colors.GREEN
    else:
        return f"{count} configured", Colors.GREEN


def get_username(config):
    """Get username with color"""
    username = config['credentials'].get('username', '')
    if username:
        return username, Colors.YELLOW
    return None


def get_password(config):
    """Get password with color"""
    password = config['credentials'].get('password', '')
    if password:
        return password, Colors.YELLOW
    return None


def has_credentials(config):
    """Check if any credentials exist"""
    username = config['credentials'].get('username', '')
    password = config['credentials'].get('password', '')
    return bool(username or password)

def get_main_menu_title(config):
    """Get dynamic title for main menu"""
    lab_name = (config['metadata'].get('name') or 
                config['metadata'].get('machine_name') or 
                config['metadata'].get('lab_name') or 
                config['metadata'].get('challenge_name') or 
                'Main Menu')
    return lab_name