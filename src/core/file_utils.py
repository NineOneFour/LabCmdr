import os
from pathlib import Path
from ..config import Colors

def check_overwrite(filepath, overwrite_mode=None):
    """
    Check if a file should be overwritten, prompting user if necessary.
    
    Args:
        filepath: Path to the file that might be overwritten (Path object or string)
        overwrite_mode: Current overwrite mode ('all', 'none', or None)
    
    Returns:
        tuple: (should_overwrite: bool, new_overwrite_mode: str or None)
            - should_overwrite: True if file should be overwritten/created, False to skip
            - new_overwrite_mode: Updated overwrite mode ('all', 'none', or None)
    """
    filepath = Path(filepath)
    
    # If file doesn't exist, no need to check - just create it
    if not filepath.exists():
        return (True, overwrite_mode)
    
    # If we already have a mode set, apply it
    if overwrite_mode == 'all':
        return (True, overwrite_mode)
    elif overwrite_mode == 'none':
        print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
        return (False, overwrite_mode)
    
    # No mode set yet, prompt the user
    print(f"\n{filepath.name} already exists. Overwrite?")
    print("  [y] Yes (this file only)")
    print("  [n] No (skip this file)")
    print("  [a] All (overwrite all remaining files)")
    print("  [s] Do not overwrite any remaining files)")
    
    while True:
        choice = input("Choice: ").lower().strip()
        
        if choice in ['y', 'yes']:
            # Overwrite this file only, don't change mode
            return (True, overwrite_mode)
        
        elif choice in ['n', 'no']:
            # Skip this file only, don't change mode
            print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
            return (False, overwrite_mode)
        
        elif choice in ['a', 'all']:
            # Overwrite this and all remaining files
            return (True, 'all')
        
        elif choice in ['s', 'skip']:
            # Skip this and all remaining files
            print(f"{Colors.YELLOW}[*] Skipping {filepath.name}{Colors.NC}")
            return (False, 'none')
        
        else:
            print("Invalid choice. Please enter y, n, a, or s.")