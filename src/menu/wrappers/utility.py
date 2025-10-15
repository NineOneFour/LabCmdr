import sys
import subprocess
from ...actions.update_lab import edit_field
from ...config import Colors
from ...core.context import (
    load_lab_config,
    find_lab_root,
)


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



def wrap_open_notes(config):
    """Open notes directory"""

    
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




__all__ = [
    "wrap_edit_metadata_field",
    "wrap_edit_network_field",
    "wrap_edit_credentials_field",
    "wrap_open_notes",
    "wrap_open_scans",
    "wrap_show_lab_info",
] 