#!/usr/bin/env python3
"""
update_lab.py - Lab configuration management functions
Pure functions for editing labconfig.json - no menu logic
"""

import sys
import termios
import tty
from datetime import datetime

from ..config import Colors
from ..core.context import load_lab_config, save_lab_config
from ..utils import menu_utils


# =========================
# ESC-aware Input Function
# =========================
def get_input_with_escape(prompt="", current_value=""):
    """
    Reads input while allowing ESC to cancel.
    
    Args:
        prompt: The prompt text to display
        current_value: Current value to show (optional)
    
    Returns:
        User input string, or None if ESC pressed
    """
    if current_value:
        print(f"{Colors.YELLOW}Current: {current_value}{Colors.NC}")
    print(prompt, end="", flush=True)
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        user_input = ""
        while True:
            ch = sys.stdin.read(1)
            if ch == "\x1b":  # ESC
                print(f"\n{Colors.YELLOW}[*] Cancelled{Colors.NC}")
                return None
            elif ch in ("\r", "\n"):
                print()
                break
            elif ch == "\x7f":  # Backspace
                if user_input:
                    user_input = user_input[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                user_input += ch
                sys.stdout.write(ch)
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return user_input.strip()


# =========================
# Field Editing Functions
# =========================
def edit_field(section, key, config=None):
    """
    Edit a single field in the config.
    Saves immediately upon successful change.
    
    Args:
        section: Config section name (e.g., 'metadata', 'network', 'credentials')
        key: Field key within the section
        config: Optional config dict (loads if not provided)
    
    Returns:
        bool: True if field was updated, False if cancelled or no change
    """
    if config is None:
        config = load_lab_config()
    
    print(f"\n{Colors.CYAN}Editing {section} → {key}{Colors.NC}\n")
    
    current = config[section][key]
    if current is None or current == "":
        current = "Not set"
    
    # Special handling for different field types
    if key == "ip_address":
        prompt = "Enter IP address (e.g., 10.10.10.1): "
    elif key == "year":
        prompt = f"Enter year (default: {datetime.now().year}): "
    elif "password" in key.lower():
        prompt = "Enter password: "
    else:
        prompt = f"Enter {key.replace('_', ' ')}: "
    
    new_val = get_input_with_escape(prompt, str(current))
    
    if new_val is None:
        return False  # Cancelled
    
    if new_val:
        # Type conversion for specific fields
        if key == "year" and new_val.isdigit():
            new_val = int(new_val)
        elif key in ["season", "week"] and new_val.isdigit():
            new_val = int(new_val)
        
        config[section][key] = new_val
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] Updated {key} to: {new_val}{Colors.NC}")
        return True
    else:
        print(f"{Colors.YELLOW}[*] No change made{Colors.NC}")
        return False


def quick_ip_update(config=None):
    """
    Quick update for IP address.
    
    Returns:
        bool: True if updated, False if cancelled/no change
    """
    config = load_lab_config()
    
    print(f"\n{Colors.CYAN}Quick IP Update{Colors.NC}\n")
    
    current_ip = config["network"].get("ip_address", "Not set")
    
    new_ip = get_input_with_escape("Enter new IP (ESC to cancel): ", current_ip)
    
    if new_ip is None:
        return False
    
    if new_ip:
        config["network"]["ip_address"] = new_ip
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] IP updated to: {new_ip}{Colors.NC}")
        return True
    else:
        print(f"{Colors.YELLOW}[*] No change made{Colors.NC}")
        return False


# =========================
# FQDN Management Functions
# =========================
def add_fqdn(fqdn=None):
    """
    Add a new FQDN to the list.
    
    Args:
        fqdn: FQDN string to add (prompts if not provided)
    
    Returns:
        bool: True if added, False if cancelled
    """
    config = load_lab_config()
    fqdn_list = config["network"].get("fqdn", [])
    
    if fqdn is None:
        fqdn = get_input_with_escape("Enter new FQDN (e.g., box.htb): ")
    
    if fqdn:
        fqdn_list.append(fqdn)
        config["network"]["fqdn"] = fqdn_list
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] Added {fqdn}{Colors.NC}")
        return True
    
    return False


def remove_fqdn(fqdn=None, index=None):
    """
    Remove an FQDN from the list.
    
    Args:
        fqdn: FQDN string to remove (searches list)
        index: Index to remove (if known)
    
    Returns:
        bool: True if removed, False if not found or cancelled
    """
    config = load_lab_config()
    fqdn_list = config["network"].get("fqdn", [])
    
    if not fqdn_list:
        print(f"{Colors.YELLOW}[!] No FQDNs configured{Colors.NC}")
        return False
    
    # If neither fqdn nor index provided, show list and prompt
    if fqdn is None and index is None:
        print(f"\n{Colors.CYAN}Current FQDNs:{Colors.NC}")
        for i, f in enumerate(fqdn_list, 1):
            print(f"  {Colors.GREEN}[{i}]{Colors.NC} {f}")
        
        idx_input = get_input_with_escape("\nEnter number to remove (ESC to cancel): ")
        if idx_input is None:
            return False
        
        if idx_input.isdigit():
            index = int(idx_input) - 1
        else:
            print(f"{Colors.RED}[!] Invalid input{Colors.NC}")
            return False
    
    # Remove by index
    if index is not None:
        if 0 <= index < len(fqdn_list):
            removed = fqdn_list.pop(index)
            config["network"]["fqdn"] = fqdn_list
            save_lab_config(config)
            print(f"{Colors.GREEN}[+] Removed {removed}{Colors.NC}")
            return True
        else:
            print(f"{Colors.RED}[!] Invalid index{Colors.NC}")
            return False
    
    # Remove by value
    if fqdn in fqdn_list:
        fqdn_list.remove(fqdn)
        config["network"]["fqdn"] = fqdn_list
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] Removed {fqdn}{Colors.NC}")
        return True
    else:
        print(f"{Colors.RED}[!] FQDN not found: {fqdn}{Colors.NC}")
        return False


def list_fqdns():
    """
    Display all configured FQDNs.
    
    Returns:
        list: List of FQDN strings
    """
    config = load_lab_config()
    fqdn_list = config["network"].get("fqdn", [])
    
    if not fqdn_list:
        print(f"\n{Colors.YELLOW}No FQDNs configured{Colors.NC}")
        return []
    
    print(f"\n{Colors.CYAN}Configured FQDNs:{Colors.NC}")
    for i, fqdn in enumerate(fqdn_list, 1):
        print(f"  {Colors.GREEN}[{i}]{Colors.NC} {fqdn}")
    
    return fqdn_list


# =========================
# View Configuration
# =========================
def view_config(config=None):
    """
    Display the current configuration.
    
    Args:
        config: Optional config dict (loads if not provided)
    """
    if config is None:
        config = load_lab_config()
    
    menu_utils.print_title("Current Configuration","CYAN")
    
    # Metadata section
    print(f"{Colors.CYAN}═══ Metadata ═══{Colors.NC}")
    for key, value in config["metadata"].items():
        if value and key not in ['created', 'type', 'platform']:
            display_key = key.replace('_', ' ').title()
            print(f"  {display_key}: {Colors.YELLOW}{value}{Colors.NC}")
    
    # Network section
    print(f"\n{Colors.CYAN}═══ Network ═══{Colors.NC}")
    for key, value in config["network"].items():
        if value:
            display_key = key.replace('_', ' ').title()
            if isinstance(value, list):
                print(f"  {display_key}:")
                for item in value:
                    print(f"    • {Colors.YELLOW}{item}{Colors.NC}")
            else:
                print(f"  {display_key}: {Colors.YELLOW}{value}{Colors.NC}")
    
    # Credentials section
    print(f"\n{Colors.CYAN}═══ Credentials ═══{Colors.NC}")
    for key, value in config["credentials"].items():
        if value:
            display_key = key.replace('_', ' ').title()
            print(f"  {display_key}: {Colors.YELLOW}{value}{Colors.NC}")
    
    print()


# =========================
# Batch Update Functions
# =========================
def update_metadata(updates):
    """
    Update multiple metadata fields at once.
    
    Args:
        updates: Dict of key-value pairs to update
    
    Returns:
        bool: True if any updates made
    """
    config = load_lab_config()
    changed = False
    
    for key, value in updates.items():
        if key in config["metadata"]:
            config["metadata"][key] = value
            changed = True
    
    if changed:
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] Metadata updated{Colors.NC}")
    
    return changed


def update_network(updates):
    """
    Update multiple network fields at once.
    
    Args:
        updates: Dict of key-value pairs to update
    
    Returns:
        bool: True if any updates made
    """
    config = load_lab_config()
    changed = False
    
    for key, value in updates.items():
        if key in config["network"]:
            config["network"][key] = value
            changed = True
    
    if changed:
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] Network settings updated{Colors.NC}")
    
    return changed


def update_credentials(updates):
    """
    Update credential fields.
    
    Args:
        updates: Dict of key-value pairs to update
    
    Returns:
        bool: True if any updates made
    """
    config = load_lab_config()
    changed = False
    
    for key, value in updates.items():
        if key in config["credentials"]:
            config["credentials"][key] = value
            changed = True
    
    if changed:
        save_lab_config(config)
        print(f"{Colors.GREEN}[+] Credentials updated{Colors.NC}")
    
    return changed