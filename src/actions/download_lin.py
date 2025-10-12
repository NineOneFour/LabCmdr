#!/usr/bin/env python3
"""
download_lin.py - Linux enumeration tools downloader
Downloads and manages Linux-specific enumeration tools
"""

import os
import urllib.request
from pathlib import Path

from ..config import Colors
from ..core.context import find_lab_root


# Linux tools dictionary
LINUX_TOOLS = {
    "linpeas.sh": "https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh",
    "pspy64": "https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64",
    "pspy32": "https://github.com/DominicBreuker/pspy/releases/latest/download/pspy32",
    "linenum.sh": "https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh",
    "lse.sh": "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh",
}


def download_file(url, destination):
    """
    Download a file from URL to destination.
    
    Args:
        url: URL to download from
        destination: Local file path to save to
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"{Colors.YELLOW}[*] Downloading {os.path.basename(destination)}...{Colors.NC}")
        urllib.request.urlretrieve(url, destination)
        os.chmod(destination, 0o755)  # Make executable
        print(f"{Colors.GREEN}[+] {os.path.basename(destination)} downloaded successfully{Colors.NC}")
        return True
    except Exception as e:
        print(f"{Colors.RED}[!] Failed to download {os.path.basename(destination)}: {e}{Colors.NC}")
        return False


def download_linux_tools(force=False):
    """
    Download all Linux enumeration tools to current lab's tools directory.
    
    Args:
        force: If True, re-download even if files exist
    
    Returns:
        list: Paths to downloaded tools
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    # Create tools directory if it doesn't exist
    tools_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║       Downloading Linux Tools            ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    downloaded = []
    skipped = []
    failed = []
    
    for filename, url in LINUX_TOOLS.items():
        dest = tools_dir / filename
        
        # Check if file exists and skip if not forcing
        if dest.exists() and not force:
            print(f"{Colors.GREEN}[+] {filename} already exists, skipping{Colors.NC}")
            skipped.append(str(dest))
            continue
        
        # Download the file
        if download_file(url, str(dest)):
            downloaded.append(str(dest))
        else:
            failed.append(filename)
    
    # Print summary
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Download Summary                 ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    if downloaded:
        print(f"{Colors.GREEN}Downloaded ({len(downloaded)}):{Colors.NC}")
        for path in downloaded:
            print(f"  • {Path(path).name}")
    
    if skipped:
        print(f"\n{Colors.YELLOW}Skipped ({len(skipped)}):{Colors.NC}")
        for path in skipped:
            print(f"  • {Path(path).name}")
    
    if failed:
        print(f"\n{Colors.RED}Failed ({len(failed)}):{Colors.NC}")
        for name in failed:
            print(f"  • {name}")
    
    print(f"\n{Colors.GREEN}[+] Linux tools preparation complete{Colors.NC}")
    print(f"{Colors.CYAN}Tools location: {tools_dir}{Colors.NC}\n")
    
    return downloaded


def list_linux_tools():
    """
    List all available Linux tools and their download status.
    
    Returns:
        dict: Tool status information
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Available Linux Tools            ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    status = {}
    
    for filename, url in LINUX_TOOLS.items():
        dest = tools_dir / filename
        exists = dest.exists()
        
        status[filename] = {
            "exists": exists,
            "path": str(dest) if exists else None,
            "url": url
        }
        
        # Display status
        if exists:
            size = dest.stat().st_size
            size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"
            print(f"  {Colors.GREEN}✓{Colors.NC} {filename:<20} ({size_str})")
        else:
            print(f"  {Colors.RED}✗{Colors.NC} {filename:<20} (not downloaded)")
    
    print(f"\n{Colors.CYAN}Tools directory: {tools_dir}{Colors.NC}\n")
    
    return status


def remove_linux_tools():
    """
    Remove all downloaded Linux tools.
    
    Returns:
        int: Number of tools removed
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    print(f"\n{Colors.YELLOW}[!] This will remove all Linux tools{Colors.NC}")
    print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
    
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return 0
    
    removed = 0
    
    for filename in LINUX_TOOLS.keys():
        dest = tools_dir / filename
        if dest.exists():
            try:
                dest.unlink()
                print(f"{Colors.GREEN}[+] Removed {filename}{Colors.NC}")
                removed += 1
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to remove {filename}: {e}{Colors.NC}")
    
    if removed > 0:
        print(f"\n{Colors.GREEN}[+] Removed {removed} Linux tools{Colors.NC}")
    else:
        print(f"\n{Colors.YELLOW}[*] No Linux tools found to remove{Colors.NC}")
    
    return removed