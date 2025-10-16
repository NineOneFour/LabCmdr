import os
import urllib.request
from pathlib import Path

from .tools import (
    WINDOWS_TOOLS,
    LINUX_TOOLS,
    AD_TOOLS,
)

from ..config import Colors
from ..core.context import find_lab_root



TOOL_PATH = find_lab_root() / "server" / "serve" / "tools" / "tools"

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
        print(f"{Colors.GREEN}[+] {os.path.basename(destination)} downloaded successfully{Colors.NC}")
        return True
    except Exception as e:
        print(f"{Colors.RED}[!] Failed to download {os.path.basename(destination)}: {e}{Colors.NC}")
        return False
    
def download_tools(toolset, force=False):
    """
    Download all Active Directory enumeration tools to current lab's tools directory.
    These tools are meant to be transferred to and run on target Windows machines.
    
    Args:
        force: If True, re-download even if files exist
    
    Returns:
        list: Paths to downloaded tools
    """

    if toolset == "windows":
        tools_dict = WINDOWS_TOOLS
        tool_type = "Available Windows Tools"
    elif toolset == "linux":
        tools_dict = LINUX_TOOLS
        tool_type = "Avalable Linux Tools"
    elif toolset == "ad":
        tools_dict = AD_TOOLS
        tool_type = "Available AD Tools"
    elif toolset == "all":
        tools_dict = {**WINDOWS_TOOLS, **LINUX_TOOLS, **AD_TOOLS}
        tool_type = "All Available Tools"
    else:
        print(f"{Colors.RED}[!] Unknown toolset: {toolset}{Colors.NC}")
        return []

    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    # Create tools directory if it doesn't exist
    tools_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")

    print(f"{Colors.BLUE}║       Downloading {tool_type} Tools               ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.CYAN}[*] These tools run ON target Windows machines{Colors.NC}")
    print(f"{Colors.CYAN}[*] BloodHound GUI should be installed on your attacking machine{Colors.NC}\n")
    
    downloaded = []
    skipped = []
    failed = []
    
    for filename, url in tools_dict.items():
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
    
    return downloaded

