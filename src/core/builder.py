import os
import yaml, json
from pathlib import Path
from datetime import datetime
from .file_utils import check_overwrite
from ..config import Colors, LAB_CONFIG
from ..templates.structure import STRUCTURE
from .copy_files import copy_files


def save_context(context, lab_path):
    """Save context as yaml to .labconfig in the lab folder"""
    # Create a copy of the LAB_CONFIG structure
    config = json.loads(json.dumps(LAB_CONFIG))  # Deep copy
    
    # Populate metadata section
    metadata = config['metadata']
    metadata['name'] = context.get('machine_name', context.get('lab_name', context.get('challenge_name', '')))
    metadata['platform'] = context.get('platform', context.get('custom_platform', ''))
    metadata['type'] = context.get('type', '')
    metadata['created'] = datetime.now().isoformat()
    metadata['season'] = context.get('season')
    metadata['week'] = context.get('week')
    metadata['conference'] = context.get('conference', '')
    metadata['conference_name'] = context.get('conference_name', '')
    metadata['village'] = context.get('village', '')
    metadata['location'] = context.get('location', '')
    metadata['year'] = context.get('year')
    metadata['challenge_name'] = context.get('challenge_name', '')
    metadata['category'] = context.get('category', '')
    
    # Populate network section
    config['network']['ip_address'] = context.get('ip_address')
    # Leave domain, domain_name, domain_controller, and fqdn empty - filled later
    
    # Populate credentials section if provided
    if context.get('has_credentials') == 'yes':
        config['credentials']['username'] = context.get('username', '')
        config['credentials']['password'] = context.get('password', '')
    
    # Create the labcmdr directory if it doesn't exist
    config_path = Path(lab_path) / 'labcmdr' / 'labconfig.yaml'
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the config
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"{Colors.GREEN}[+] Saved configuration to labcmdr/labconfig.yaml{Colors.NC}")

def create_structure(dir_path, structure=None, overwrite_mode=None):
    """
    Creates a folder structure with files based on the STRUCTURE dictionary.
    
    Args:
        dir_path: Base directory path where structure will be created
        structure: Dictionary defining the folder/file structure (uses STRUCTURE if None)
        overwrite_mode: Internal parameter to track user's overwrite choice ('all', 'none', or None)
    
    Returns:
        overwrite_mode: The current overwrite mode (for recursive calls)
    """
    if structure is None:
        from ..templates.structure import STRUCTURE
        structure = STRUCTURE
    
    # Create the base directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)
    
    for name, content in structure.items():
        path = os.path.join(dir_path, name)
        
        # If content is a dict, it's a directory (possibly with nested content)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            # Recursively create nested structure
            if content:  # If the dict is not empty
                overwrite_mode = create_structure(path, content, overwrite_mode)
        
        # If content is None or a string, it's a file
        else:
            # Check if file should be overwritten
            should_overwrite, overwrite_mode = check_overwrite(path, overwrite_mode)
            
            if not should_overwrite:
                continue
            
            # Create the file (empty for now, or with content if provided as string)
            try:
                with open(path, 'w') as f:
                    if isinstance(content, str):
                        f.write(content)
                    # else: create empty file (content is None)
                print(f"{Colors.GREEN}[+] Created: {name}{Colors.NC}")
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to create {name}: {e}{Colors.NC}")
    
    return overwrite_mode