import shutil
from pathlib import Path
from .file_utils import check_overwrite
from ..config import Colors
from ..templates.structure import COPYFILES

def copy_files(base_path, copyfiles=None, overwrite_mode=None):
    """
    Copies files from lab-setup directory to the new lab structure.
    
    Args:
        base_path: Base directory path where files will be copied to
        copyfiles: Dictionary mapping source paths to destination paths (uses COPYFILES if None)
        overwrite_mode: Overwrite mode from create_structure ('all', 'none', or None)
    
    Returns:
        overwrite_mode: The current overwrite mode (for consistency with create_structure)
    """
    if copyfiles is None:
        from ..templates.structure import COPYFILES
        copyfiles = COPYFILES
    
    # Auto-detect lab-setup directory (where this script lives)
    script_dir = Path(__file__).parent.parent.resolve()
    
    for source_rel, dest_rel in copyfiles.items():
        # Construct full paths
        source_path = script_dir / source_rel
        dest_path = Path(base_path) / dest_rel
        
        # Check if source file exists
        if not source_path.exists():
            print(f"{Colors.RED}[!] Source file not found: {source_path}{Colors.NC}")
            continue
        
        # Create destination directory if it doesn't exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file should be overwritten
        should_overwrite, overwrite_mode = check_overwrite(dest_path, overwrite_mode)
        
        if not should_overwrite:
            continue
        
        # Copy the file
        try:
            shutil.copy2(source_path, dest_path)  # copy2 preserves metadata
            print(f"{Colors.GREEN}[+] Copied: {source_rel} -> {dest_rel}{Colors.NC}")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to copy {source_rel}: {e}{Colors.NC}")
    
    return overwrite_mode