#!/usr/bin/env python3
"""
config_manager.py - Configuration loading and management
Handles loading, merging, and accessing global and lab-specific configs
"""

import os
import yaml
from pathlib import Path
from ..config import Colors


# Default config values (fallback if files don't exist)
DEFAULT_CONFIG = {
    "paths": {
        "labs_root": str(Path.home() / "Labs"),
        "config_dir": str(Path.home() / ".config" / "labcmdr")
    },
    "network": {
        "interface": "tun0",
        "fallback_interfaces": ["tun1", "eth0"],
        "auto_detect": False
    },
    "server": {
        "default_port": 8080,
        "auto_increment_port": True,
        "enable_upload": True,
        "serve_directory": "server/serve",
        "loot_directory": "server/loot"
    },
    "scanning": {
        "tool": "nmap",
        "initial_scan_flags": "-sC -sV -oN scans/nmap/initial.txt",
        "full_scan_flags": "-p- -sC -sV -oN scans/nmap/full.txt",
        "udp_scan_flags": "-sU --top-ports 100 -oN scans/nmap/udp.txt"
    },
    "tools": {
        "auto_download": False,
        "categories": ["linux", "windows"]
    },
    "platforms": {
        "htb": {
            "current_season": 9
        }
    },
    "behavior": {
        "file_overwrite": "prompt",
        "auto_update_hosts": False,
        "confirm_destructive": True
    },
    "applications": {
        "editor": "nano",
        "file_manager": "xdg-open",
        "terminal": "x-terminal-emulator"
    },
    "system": {
        "hosts_file": "/etc/hosts",
        "use_sudo_for_hosts": True
    }
}


def expand_path(path_str):
    """
    Expand environment variables and user home in path strings.
    
    Args:
        path_str: Path string that may contain $HOME, ~, or env vars
    
    Returns:
        Expanded absolute path as string
    """
    if not path_str:
        return path_str
    
    # Expand environment variables
    expanded = os.path.expandvars(path_str)
    # Expand user home
    expanded = os.path.expanduser(expanded)
    # Convert to absolute path
    expanded = str(Path(expanded).resolve())
    
    return expanded


def load_yaml_config(config_path):
    """
    Load YAML config file.
    
    Args:
        config_path: Path to YAML config file
    
    Returns:
        Dictionary of config values, or None if file doesn't exist
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        return None
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config if config else {}
    except yaml.YAMLError as e:
        print(f"{Colors.YELLOW}[!] Warning: Error parsing {config_path}: {e}{Colors.NC}")
        print(f"{Colors.CYAN}[*] Using default configuration{Colors.NC}")
        return None
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Warning: Could not read {config_path}: {e}{Colors.NC}")
        return None


def merge_configs(base, override):
    """
    Recursively merge two config dictionaries.
    Values in override take precedence over base.
    
    Args:
        base: Base configuration dictionary
        override: Override configuration dictionary
    
    Returns:
        Merged configuration dictionary
    """
    if override is None:
        return base
    
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dicts
            result[key] = merge_configs(result[key], value)
        else:
            # Override value
            result[key] = value
    
    return result


def expand_paths_in_config(config):
    """
    Expand all path strings in config recursively.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Configuration with expanded paths
    """
    result = {}
    
    for key, value in config.items():
        if isinstance(value, dict):
            # Recursively expand nested dicts
            result[key] = expand_paths_in_config(value)
        elif isinstance(value, str) and ('$' in value or '~' in value or key.endswith('_root') or key.endswith('_dir') or key.endswith('_directory') or key.endswith('_file')):
            # Expand if it looks like a path
            result[key] = expand_path(value)
        else:
            result[key] = value
    
    return result


def load_global_config():
    """
    Load global configuration from ~/.config/labcmdr/config.yaml
    Falls back to defaults if file doesn't exist.
    
    Returns:
        Global configuration dictionary
    """
    config_path = Path.home() / ".config" / "labcmdr" / "config.yaml"
    
    # Try to load user config
    user_config = load_yaml_config(config_path)
    
    # Merge with defaults
    if user_config:
        config = merge_configs(DEFAULT_CONFIG, user_config)
    else:
        config = DEFAULT_CONFIG.copy()
    
    # Expand all paths
    config = expand_paths_in_config(config)
    
    return config


def get_config_value(key_path, default=None, lab_config=None):
    """
    Get a configuration value by dot-notation key path.
    Checks lab config first, then global config, then default.
    
    Args:
        key_path: Dot-notation path to config value (e.g., "server.default_port")
        default: Default value if key not found
        lab_config: Optional lab-specific config to check first
    
    Returns:
        Configuration value
    
    Examples:
        get_config_value("server.default_port")
        get_config_value("paths.labs_root")
        get_config_value("network.interface")
    """
    global_config = load_global_config()
    
    # Split key path
    keys = key_path.split('.')
    
    # Try lab config first if provided
    if lab_config:
        value = lab_config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            pass  # Fall through to global config
    
    # Try global config
    value = global_config
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def get_labs_root():
    """Convenience function to get labs root directory"""
    return get_config_value("paths.labs_root")


def get_network_interface():
    """Convenience function to get primary network interface"""
    return get_config_value("network.interface")


def get_fallback_interfaces():
    """Convenience function to get fallback network interfaces"""
    return get_config_value("network.fallback_interfaces", [])


def get_default_port():
    """Convenience function to get default server port"""
    return get_config_value("server.default_port", 8080)


def get_htb_season():
    """Convenience function to get current HTB season"""
    return get_config_value("platforms.htb.current_season", 9)


def validate_config(config):
    """
    Validate configuration values.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check labs_root exists or can be created
    labs_root = Path(config['paths']['labs_root'])
    if not labs_root.exists():
        try:
            labs_root.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create labs_root directory: {e}")
    
    # Check port is valid
    port = config['server']['default_port']
    if not isinstance(port, int) or port < 1 or port > 65535:
        errors.append(f"Invalid port number: {port} (must be 1-65535)")
    
    # Check editor exists
    import shutil
    editor = config['applications']['editor']
    if not shutil.which(editor):
        errors.append(f"Editor '{editor}' not found in PATH")
    
    return (len(errors) == 0, errors)