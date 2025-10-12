import os
from pathlib import Path
from ..config import Colors
from ..core.config_manager import get_config_value

def check_overwrite(filepath, overwrite_mode=None):
    """
    Check if a file should be overwritten, prompting user if necessary.
    
    Args:
        filepath: Path to the file that might be overwritten (Path object or string)
        overwrite_mode: Current overwrite mode ('all', 'none', or None)
                       If None, uses config default
    
    Returns:
        tuple: (should_overwrite: bool, new_overwrite_mode: str or None)
    """
    filepath = Path(filepath)
    
    # If file doesn't exist, no need to check - just create it
    if not filepath.exists():
        return (True, overwrite_mode)
    
    # If we already have a mode set from previous prompts, apply it
    if overwrite_mode == 'all':
        return (True, overwrite_mode)
    elif overwrite_mode == 'none':
        print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
        return (False, overwrite_mode)
    
    # No mode set yet - check config for default behavior
    if overwrite_mode is None:
        config_behavior = get_config_value("behavior.file_overwrite", "prompt")
        
        if config_behavior == "all":
            return (True, overwrite_mode)  # Don't change mode, just overwrite this file
        elif config_behavior == "none":
            print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
            return (False, overwrite_mode)  # Don't change mode, just skip this file
        # If "prompt", fall through to prompt below
    
    # Prompt the user
    print(f"\n{filepath.name} already exists. Overwrite?")
    print("  [y] Yes (this file only)")
    print("  [n] No (skip this file)")
    print("  [a] All (overwrite all remaining files)")
    print("  [s] Skip (do not overwrite any remaining files)")
    
    while True:
        choice = input("Choice: ").lower().strip()
        
        if choice in ['y', 'yes']:
            return (True, overwrite_mode)
        
        elif choice in ['n', 'no']:
            print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
            return (False, overwrite_mode)
        
        elif choice in ['a', 'all']:
            return (True, 'all')
        
        elif choice in ['s', 'skip']:
            print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
            return (False, 'none')
        
        else:
            print("Invalid choice. Please enter y, n, a, or s.")