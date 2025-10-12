#!/usr/bin/env python3
"""
config.py - Configuration management command
Interactive menu and CLI interface for managing global config
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

from ..config import Colors
from ..core.config_manager import (
    load_global_config,
    get_config_value,
    validate_config,
    DEFAULT_CONFIG,
    expand_path
)


def get_config_path():
    """Get path to user config file"""
    return Path.home() / ".config" / "labcmdr" / "config.yaml"


def get_default_config_path():
    """Get path to default config template in repo"""
    # Navigate from this file to src/templates/default_config.yaml
    return Path(__file__).parent.parent / "templates" / "default_config.yaml"


def show_config():
    """Display current configuration"""
    config = load_global_config()
    config_path = get_config_path()
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Current Configuration            ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.CYAN}Config file: {Colors.YELLOW}{config_path}{Colors.NC}\n")
    
    # Display each section
    for section, values in config.items():
        print(f"{Colors.CYAN}[{section}]{Colors.NC}")
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, list):
                    print(f"  {key}:")
                    for item in value:
                        print(f"    - {Colors.YELLOW}{item}{Colors.NC}")
                else:
                    print(f"  {key}: {Colors.YELLOW}{value}{Colors.NC}")
        else:
            print(f"  {Colors.YELLOW}{values}{Colors.NC}")
        print()


def get_value(key_path):
    """Get a specific config value"""
    value = get_config_value(key_path)
    
    if value is None:
        print(f"{Colors.RED}[!] Key not found: {key_path}{Colors.NC}")
        return
    
    print(f"{Colors.CYAN}{key_path}:{Colors.NC} {Colors.YELLOW}{value}{Colors.NC}")


def set_value(key_path, new_value):
    """Set a specific config value"""
    import yaml
    
    config_path = get_config_path()
    
    # Load current config
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"{Colors.RED}[!] Config file not found. Run 'labcmdr config init' first{Colors.NC}")
        return
    
    # Split key path and navigate to correct location
    keys = key_path.split('.')
    current = config
    
    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the value
    final_key = keys[-1]
    
    # Try to convert value to appropriate type
    if new_value.lower() in ['true', 'false']:
        new_value = new_value.lower() == 'true'
    elif new_value.isdigit():
        new_value = int(new_value)
    elif new_value.startswith('[') and new_value.endswith(']'):
        # Simple list parsing
        new_value = [item.strip() for item in new_value[1:-1].split(',')]
    
    current[final_key] = new_value
    
    # Save config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"{Colors.GREEN}[+] Updated {key_path} = {new_value}{Colors.NC}")
    except Exception as e:
        print(f"{Colors.RED}[!] Failed to save config: {e}{Colors.NC}")


def edit_config():
    """Open config file in editor"""
    config_path = get_config_path()
    
    if not config_path.exists():
        print(f"{Colors.YELLOW}[!] Config file doesn't exist yet{Colors.NC}")
        print(f"{Colors.CYAN}[*] Run 'labcmdr config init' to create it{Colors.NC}")
        return
    
    # Get editor from config (with fallback)
    editor = get_config_value("applications.editor", "nano")
    
    # Check if editor exists
    if not shutil.which(editor):
        print(f"{Colors.RED}[!] Editor '{editor}' not found{Colors.NC}")
        editor = "nano"  # Fallback to nano
    
    print(f"{Colors.CYAN}[*] Opening config in {editor}...{Colors.NC}")
    
    try:
        subprocess.run([editor, str(config_path)])
        print(f"{Colors.GREEN}[+] Config saved{Colors.NC}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error opening editor: {e}{Colors.NC}")


def init_config(use_existing=False):
    """Initialize or reset config file"""
    config_path = get_config_path()
    default_config_path = get_default_config_path()
    
    if not default_config_path.exists():
        print(f"{Colors.RED}[!] Default config template not found at {default_config_path}{Colors.NC}")
        return
    
    # Check if config already exists
    if config_path.exists() and not use_existing:
        print(f"{Colors.YELLOW}[!] Config file already exists at {config_path}{Colors.NC}")
        print(f"\n{Colors.CYAN}Options:{Colors.NC}")
        print(f"  - Use 'labcmdr config edit' to modify existing config")
        print(f"  - Use 'labcmdr config reset' to reset to defaults")
        return
    
    # Create config directory if needed
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy default config with environment variable substitution
    try:
        # Read default config
        with open(default_config_path, 'r') as f:
            content = f.read()
        
        # Expand $HOME
        content = content.replace('$HOME', str(Path.home()))
        
        # Write to user config
        with open(config_path, 'w') as f:
            f.write(content)
        
        print(f"{Colors.GREEN}[+] Config file created at {config_path}{Colors.NC}")
        
        # Optionally open in editor
        if use_existing:
            print(f"\n{Colors.CYAN}Edit now? (y/n):{Colors.NC} ", end="")
            if input().strip().lower() == 'y':
                edit_config()
    
    except Exception as e:
        print(f"{Colors.RED}[!] Failed to create config: {e}{Colors.NC}")


def reset_config():
    """Reset config to defaults"""
    config_path = get_config_path()
    
    print(f"{Colors.YELLOW}[!] This will reset your config to defaults{Colors.NC}")
    print(f"{Colors.RED}[!] Your current settings will be lost{Colors.NC}")
    print(f"\n{Colors.CYAN}Continue? (y/n):{Colors.NC} ", end="")
    
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return
    
    # Backup existing config
    if config_path.exists():
        backup_path = config_path.with_suffix('.yaml.backup')
        shutil.copy2(config_path, backup_path)
        print(f"{Colors.GREEN}[+] Backed up to {backup_path}{Colors.NC}")
    
    # Initialize with defaults
    init_config(use_existing=True)


def show_path():
    """Show path to config file"""
    config_path = get_config_path()
    exists = config_path.exists()
    
    print(f"\n{Colors.CYAN}Config file location:{Colors.NC}")
    print(f"  {Colors.YELLOW}{config_path}{Colors.NC}")
    print(f"\n{Colors.CYAN}Status:{Colors.NC} ", end="")
    
    if exists:
        print(f"{Colors.GREEN}✓ Exists{Colors.NC}")
    else:
        print(f"{Colors.RED}✗ Not found{Colors.NC}")
        print(f"\n{Colors.CYAN}Run 'labcmdr config init' to create it{Colors.NC}")


def validate_config_file():
    """Validate config file"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Config Validation                ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    config = load_global_config()
    is_valid, errors = validate_config(config)
    
    if is_valid:
        print(f"{Colors.GREEN}[+] Configuration is valid{Colors.NC}")
    else:
        print(f"{Colors.RED}[!] Configuration has errors:{Colors.NC}\n")
        for error in errors:
            print(f"  • {Colors.YELLOW}{error}{Colors.NC}")


def config_cli(args):
    """
    CLI interface for config management
    
    Args:
        args: Parsed command-line arguments
    """
    if not args.config_command:
        # No subcommand - show interactive menu
        config_menu()
        return
    
    cmd = args.config_command
    
    if cmd == "show":
        show_config()
    
    elif cmd == "get":
        if not args.key:
            print(f"{Colors.RED}[!] Usage: labcmdr config get <key>{Colors.NC}")
            print(f"{Colors.CYAN}Example: labcmdr config get paths.labs_root{Colors.NC}")
            return
        get_value(args.key)
    
    elif cmd == "set":
        if not args.key or not args.value:
            print(f"{Colors.RED}[!] Usage: labcmdr config set <key> <value>{Colors.NC}")
            print(f"{Colors.CYAN}Example: labcmdr config set paths.labs_root /custom/path{Colors.NC}")
            return
        set_value(args.key, args.value)
    
    elif cmd == "edit":
        edit_config()
    
    elif cmd == "init":
        init_config()
    
    elif cmd == "reset":
        reset_config()
    
    elif cmd == "path":
        show_path()
    
    elif cmd == "validate":
        validate_config_file()
    
    else:
        print(f"{Colors.RED}[!] Unknown command: {cmd}{Colors.NC}")


def config_menu():
    """Interactive config management menu"""
    from ..menu import run_menu
    from ..menu.context import submenu_header
    
    # Load config for display
    config = load_global_config()
    config_path = get_config_path()
    exists = config_path.exists()
    
    menu = {
        "title": "Configuration Management",
        "context": {
            "title": "",
            "fields": [
                ("Config File", (str(config_path), Colors.YELLOW)),
                ("Status", ("✓ Exists" if exists else "✗ Not Found", Colors.GREEN if exists else Colors.RED)),
            ]
        },
        "items": {
            "View": {
                "1": ("Show Configuration", lambda c: show_config()),
                "2": ("Show Config Path", lambda c: show_path()),
                "3": ("Validate Config", lambda c: validate_config_file()),
            },
            "Edit": {
                "4": ("Edit Config File", lambda c: edit_config()),
                "5": ("Get Value", lambda c: interactive_get()),
                "6": ("Set Value", lambda c: interactive_set()),
            },
            "Management": {
                "7": ("Initialize/Create Config", lambda c: init_config()),
                "8": ("Reset to Defaults", lambda c: reset_config()),
            }
        }
    }
    
    run_menu(menu, header_func=submenu_header, config=config, depth=1)


def interactive_get():
    """Interactive get value prompt"""
    print(f"\n{Colors.CYAN}Get Config Value{Colors.NC}\n")
    print(f"{Colors.YELLOW}Examples:{Colors.NC}")
    print(f"  paths.labs_root")
    print(f"  network.interface")
    print(f"  server.default_port")
    
    key = input(f"\n{Colors.CYAN}Enter key path:{Colors.NC} ").strip()
    
    if key:
        get_value(key)
    else:
        print(f"{Colors.RED}[!] No key provided{Colors.NC}")


def interactive_set():
    """Interactive set value prompt"""
    print(f"\n{Colors.CYAN}Set Config Value{Colors.NC}\n")
    print(f"{Colors.YELLOW}Examples:{Colors.NC}")
    print(f"  paths.labs_root = /custom/path")
    print(f"  network.interface = eth0")
    print(f"  server.default_port = 9000")
    
    key = input(f"\n{Colors.CYAN}Enter key path:{Colors.NC} ").strip()
    
    if not key:
        print(f"{Colors.RED}[!] No key provided{Colors.NC}")
        return
    
    value = input(f"{Colors.CYAN}Enter new value:{Colors.NC} ").strip()
    
    if not value:
        print(f"{Colors.RED}[!] No value provided{Colors.NC}")
        return
    
    set_value(key, value)