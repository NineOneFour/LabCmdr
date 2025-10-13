#!/usr/bin/env python3
"""
manage_host.py - /etc/hosts file management for lab environments
Pure functions for adding/removing/viewing lab entries in /etc/hosts
Uses sudo tee for secure in-terminal authentication
"""

import subprocess

from ..config import Colors
from ..core.context import load_lab_config
from ..core.config_manager import get_config_value


HOSTS_PATH = get_config_value("system.hosts_file", "/etc/hosts")


def validate_fqdn(fqdn):
    """Validate FQDN to prevent shell injection."""
    import re
    # Only allow: letters, numbers, dots, hyphens
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]$', fqdn):
        raise ValueError(f"Invalid FQDN format: {fqdn}")
    if '..' in fqdn or fqdn.startswith('.') or fqdn.endswith('.'):
        raise ValueError(f"Invalid FQDN format: {fqdn}")
    return fqdn


def update_hosts():
    """
    Update /etc/hosts file with lab entries.
    Adds or updates entries for the current lab's FQDNs.
    
    Returns:
        bool: True if successful, False otherwise
    """
    config = load_lab_config()
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         /etc/hosts Update                ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}")
    
    lab_name = config["metadata"].get("name", "")
    ip = config["network"].get("ip_address", "")
    fqdns = config["network"].get("fqdn", [])
    
    if not lab_name:
        # Try to use any available name field
        lab_name = (config["metadata"].get("machine_name") or 
                   config["metadata"].get("lab_name") or 
                   config["metadata"].get("challenge_name") or 
                   "unnamed_lab")
    
    if not ip or not fqdns:
        print(f"\n{Colors.RED}[!] Missing required fields{Colors.NC}")
        print(f"\n{Colors.YELLOW}Required:{Colors.NC}")
        print(f"  • IP address: {'✓' if ip else '✗'}")
        print(f"  • At least one FQDN: {'✓' if fqdns else '✗'}")
        return False
    
    print(f"\n{Colors.CYAN}Lab Configuration:{Colors.NC}")
    print(f"  Name: {Colors.YELLOW}{lab_name}{Colors.NC}")
    print(f"  IP:   {Colors.YELLOW}{ip}{Colors.NC}")
    print(f"  FQDNs:")
    for fqdn in fqdns:
        print(f"    • {Colors.YELLOW}{fqdn}{Colors.NC}")
    
    print(f"\n{Colors.YELLOW}This will update /etc/hosts. Continue? (y/n):{Colors.NC} ", end="")
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return False
    
    # Read current hosts file
    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
    except PermissionError:
        print(f"{Colors.YELLOW}[*] Need sudo to read /etc/hosts{Colors.NC}")
        # Try with cat (shouldn't need sudo for reading)
        try:
            result = subprocess.run(
                ["cat", HOSTS_PATH],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.splitlines(keepends=True)
            else:
                print(f"{Colors.RED}[!] Could not read /etc/hosts{Colors.NC}")
                return False
        except:
            print(f"{Colors.RED}[!] Could not read /etc/hosts{Colors.NC}")
            return False
    except FileNotFoundError:
        lines = []
    
    # Create the new block
    start_tag = f"# LABCMDR - {lab_name}"
    end_tag = f"# END LABCMDR - {lab_name}"
    
    new_block = [f"\n{start_tag}\n"]
    for fqdn in fqdns:
        validate_fqdn(fqdn)
        new_block.append(f"{ip}\t{fqdn}\n")
    new_block.append(f"{end_tag}\n")
    
    # Remove old block if it exists
    filtered = []
    inside_block = False
    for line in lines:
        if line.strip() == start_tag:
            inside_block = True
            continue
        if inside_block:
            if line.strip() == end_tag or line.startswith("# LABCMDR -"):
                inside_block = False
                if line.strip() == end_tag:
                    continue
        if not inside_block:
            filtered.append(line)
    
    # Add new block
    filtered.extend(new_block)
    
    print(f"\n{Colors.YELLOW}[*] Updating /etc/hosts (you may be prompted for sudo password)...{Colors.NC}")
    
    try:
        # Use sudo tee to write to /etc/hosts
        # The '-' makes tee read from stdin
        process = subprocess.Popen(
            ["sudo", "tee", HOSTS_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,  # Suppress tee output
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the new content
        stdout, stderr = process.communicate(input="".join(filtered))
        
        if process.returncode == 0:
            print(f"{Colors.GREEN}[+] /etc/hosts updated successfully{Colors.NC}")
            print(f"{Colors.CYAN}[*] Added entries for:{Colors.NC}")
            for fqdn in fqdns:
                print(f"    {ip} → {fqdn}")
            return True
        else:
            print(f"{Colors.RED}[!] Failed to update /etc/hosts{Colors.NC}")
            if stderr:
                print(f"{Colors.RED}[!] Error: {stderr}{Colors.NC}")
            return False
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Update cancelled by user{Colors.NC}")
        return False
    except Exception as e:
        print(f"{Colors.RED}[!] Error updating /etc/hosts: {e}{Colors.NC}")
        return False


def remove_from_hosts():
    """
    Remove lab entries from /etc/hosts.
    
    Returns:
        bool: True if successful, False otherwise
    """
    config = load_lab_config()
    
    lab_name = config["metadata"].get("name", "")
    if not lab_name:
        lab_name = (config["metadata"].get("machine_name") or 
                   config["metadata"].get("lab_name") or 
                   config["metadata"].get("challenge_name") or 
                   "unnamed_lab")
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║      Remove from /etc/hosts              ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}")
    
    print(f"\n{Colors.CYAN}This will remove entries for lab: {Colors.YELLOW}{lab_name}{Colors.NC}")
    print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return False
    
    # Read current hosts file
    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
    except:
        # Try with cat
        try:
            result = subprocess.run(
                ["cat", HOSTS_PATH],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.splitlines(keepends=True)
            else:
                print(f"{Colors.RED}[!] Could not read /etc/hosts{Colors.NC}")
                return False
        except:
            print(f"{Colors.RED}[!] Could not read /etc/hosts{Colors.NC}")
            return False
    
    # Check if lab entries exist
    start_tag = f"# LABCMDR - {lab_name}"
    end_tag = f"# END LABCMDR - {lab_name}"
    
    has_entries = any(start_tag in line for line in lines)
    if not has_entries:
        print(f"\n{Colors.YELLOW}[*] No entries found for {lab_name} in /etc/hosts{Colors.NC}")
        return True
    
    # Remove the block
    filtered = []
    inside_block = False
    removed_count = 0
    
    for line in lines:
        if line.strip() == start_tag:
            inside_block = True
            continue
        if inside_block:
            if line.strip() == end_tag:
                inside_block = False
                continue
            else:
                removed_count += 1
                continue
        filtered.append(line)
    
    print(f"\n{Colors.YELLOW}[*] Removing {removed_count} entries...{Colors.NC}")
    print(f"{Colors.YELLOW}[*] You may be prompted for sudo password...{Colors.NC}")
    
    try:
        # Use sudo tee to write to /etc/hosts
        process = subprocess.Popen(
            ["sudo", "tee", HOSTS_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input="".join(filtered))
        
        if process.returncode == 0:
            print(f"{Colors.GREEN}[+] Successfully removed {lab_name} entries from /etc/hosts{Colors.NC}")
            return True
        else:
            print(f"{Colors.RED}[!] Failed to update /etc/hosts{Colors.NC}")
            if stderr:
                print(f"{Colors.RED}[!] Error: {stderr}{Colors.NC}")
            return False
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Removal cancelled by user{Colors.NC}")
        return False
    except Exception as e:
        print(f"{Colors.RED}[!] Error updating /etc/hosts: {e}{Colors.NC}")
        return False


def view_hosts_entries():
    """
    View current lab entries in /etc/hosts.
    
    Returns:
        list: List of entry strings found, or empty list if none
    """
    config = load_lab_config()
    
    lab_name = config["metadata"].get("name", "")
    if not lab_name:
        lab_name = (config["metadata"].get("machine_name") or 
                   config["metadata"].get("lab_name") or 
                   config["metadata"].get("challenge_name") or 
                   "unnamed_lab")
    
    print(f"\n{Colors.CYAN}Checking /etc/hosts for lab entries...{Colors.NC}")
    
    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
    except:
        # Try with cat
        try:
            result = subprocess.run(
                ["cat", HOSTS_PATH],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.splitlines(keepends=True)
            else:
                print(f"{Colors.RED}[!] Could not read /etc/hosts{Colors.NC}")
                return []
        except:
            print(f"{Colors.RED}[!] Could not read /etc/hosts{Colors.NC}")
            return []
    
    # Find lab block
    start_tag = f"# LABCMDR - {lab_name}"
    end_tag = f"# END LABCMDR - {lab_name}"
    
    inside_block = False
    entries = []
    
    for line in lines:
        if line.strip() == start_tag:
            inside_block = True
            continue
        if inside_block:
            if line.strip() == end_tag:
                break
            entries.append(line.strip())
    
    if entries:
        print(f"\n{Colors.GREEN}Found entries for {lab_name}:{Colors.NC}")
        for entry in entries:
            if entry and not entry.startswith("#"):
                print(f"  {Colors.YELLOW}{entry}{Colors.NC}")
    else:
        print(f"\n{Colors.YELLOW}No entries found for {lab_name} in /etc/hosts{Colors.NC}")
    
    # Also check for any other LABCMDR entries
    other_labs = []
    for line in lines:
        if line.startswith("# LABCMDR -") and lab_name not in line:
            other_lab = line.replace("# LABCMDR -", "").strip()
            if other_lab not in other_labs:
                other_labs.append(other_lab)
    
    if other_labs:
        print(f"\n{Colors.CYAN}Other lab entries found:{Colors.NC}")
        for lab in other_labs:
            print(f"  • {Colors.YELLOW}{lab}{Colors.NC}")
    
    return entries