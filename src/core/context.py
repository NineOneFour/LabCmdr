"""
context.py - Lab context detection and configuration management
"""

import json
from pathlib import Path
from ..config import LAB_CONFIG


class LabNotFoundError(Exception):
    """Raised when not in a lab directory"""
    pass


def find_lab_root(start_path=None):
    """
    Find lab root directory by searching for labcmdr/labconfig.json
    
    Works like git - searches current directory and all parent directories
    until it finds a labconfig.json file.
    
    Args:
        start_path: Optional starting directory (defaults to current working directory)
    
    Returns:
        Path object pointing to lab root directory
    
    Raises:
        LabNotFoundError: If no lab directory found
    """
    current = Path(start_path) if start_path else Path.cwd()
    
    # Search current directory and all parents
    for directory in [current] + list(current.parents):
        config_path = directory / "labcmdr" / "labconfig.json"
        if config_path.exists():
            return directory
    
    raise LabNotFoundError(
        "Not in a lab directory.\n"
        "Run 'labcmdr create' to create a new lab, or cd to an existing lab directory."
    )


def load_lab_config(lab_root=None):
    """
    Load labconfig.json from lab directory
    
    Args:
        lab_root: Optional lab root path. If None, will search for lab root.
    
    Returns:
        Dictionary containing lab configuration
    
    Raises:
        LabNotFoundError: If lab root not found
        FileNotFoundError: If labconfig.json doesn't exist
        json.JSONDecodeError: If labconfig.json is corrupted
    """
    if lab_root is None:
        lab_root = find_lab_root()
    
    config_path = lab_root / "labcmdr" / "labconfig.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"labconfig.json not found at {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Ensure structure matches LAB_CONFIG template
    config = ensure_config_structure(config)
    
    return config


def save_lab_config(config, lab_root=None):
    """
    Save labconfig.json to lab directory
    
    Args:
        config: Configuration dictionary to save
        lab_root: Optional lab root path. If None, will search for lab root.
    """
    if lab_root is None:
        lab_root = find_lab_root()
    
    config_path = lab_root / "labcmdr" / "labconfig.json"
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write atomically using temp file
    temp_path = config_path.with_suffix('.tmp')
    with open(temp_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    # Atomic rename
    temp_path.replace(config_path)


def ensure_config_structure(config):
    """
    Ensure config has all required fields from LAB_CONFIG template
    Adds missing fields without overwriting existing ones
    """
    def recursive_update(base, default):
        for key, val in default.items():
            if key not in base:
                base[key] = val
            elif isinstance(val, dict) and isinstance(base[key], dict):
                recursive_update(base[key], val)
        return base
    
    return recursive_update(config, LAB_CONFIG)


def get_lab_info():
    """
    Get quick summary of current lab
    
    Returns:
        Dictionary with lab name, target IP, location, etc.
    
    Raises:
        LabNotFoundError: If not in a lab directory
    """
    lab_root = find_lab_root()
    config = load_lab_config(lab_root)
    
    return {
        "name": config['metadata'].get('name', 'Unknown'),
        "location": str(lab_root),
        "target_ip": config['network'].get('ip_address'),
        "platform": config['metadata'].get('platform', 'Unknown'),
        "type": config['metadata'].get('type', 'Unknown'),
        "created": config['metadata'].get('created'),
    }