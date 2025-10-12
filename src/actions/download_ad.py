#!/usr/bin/env python3
"""
download_ad.py - Active Directory enumeration tools downloader
Downloads and manages AD-specific tools for deployment to target machines
These are tools that run ON the target Windows machines during AD enumeration
"""

import os
import urllib.request
from pathlib import Path

from ..config import Colors
from ..core.context import find_lab_root


# AD tools dictionary - Tools to deploy to target machines
AD_TOOLS = {
    "SharpHound.exe": "https://github.com/BloodHoundAD/BloodHound/raw/master/Collectors/SharpHound.exe",
    "SharpHound.ps1": "https://github.com/BloodHoundAD/BloodHound/raw/master/Collectors/SharpHound.ps1",
    "Rubeus.exe": "https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/raw/master/Rubeus.exe",
    "Certify.exe": "https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/raw/master/Certify.exe",
    "Seatbelt.exe": "https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/raw/master/Seatbelt.exe",
    "SharpUp.exe": "https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/raw/master/SharpUp.exe",
    "PowerView.ps1": "https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1",
    "Invoke-Mimikatz.ps1": "https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1",
    "ADModule.dll": "https://github.com/samratashok/ADModule/raw/master/Microsoft.ActiveDirectory.Management.dll",
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
        print(f"{Colors.GREEN}[+] {os.path.basename(destination)} downloaded successfully{Colors.NC}")
        return True
    except Exception as e:
        print(f"{Colors.RED}[!] Failed to download {os.path.basename(destination)}: {e}{Colors.NC}")
        return False


def download_ad_tools(force=False):
    """
    Download all Active Directory enumeration tools to current lab's tools directory.
    These tools are meant to be transferred to and run on target Windows machines.
    
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
    print(f"{Colors.BLUE}║       Downloading AD Tools               ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.CYAN}[*] These tools run ON target Windows machines{Colors.NC}")
    print(f"{Colors.CYAN}[*] BloodHound GUI should be installed on your attacking machine{Colors.NC}\n")
    
    downloaded = []
    skipped = []
    failed = []
    
    for filename, url in AD_TOOLS.items():
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
    
    print(f"\n{Colors.MAGENTA}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.MAGENTA}║         Quick Reference                  ║{Colors.NC}")
    print(f"{Colors.MAGENTA}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.CYAN}SharpHound (BloodHound data collection):{Colors.NC}")
    print(f"  .\\SharpHound.exe -c All")
    print(f"  Import-Module .\\SharpHound.ps1; Invoke-BloodHound -CollectionMethod All\n")
    
    print(f"{Colors.CYAN}Rubeus (Kerberos abuse):{Colors.NC}")
    print(f"  .\\Rubeus.exe kerberoast")
    print(f"  .\\Rubeus.exe asreproast\n")
    
    print(f"{Colors.CYAN}Certify (Certificate abuse):{Colors.NC}")
    print(f"  .\\Certify.exe find /vulnerable\n")
    
    print(f"{Colors.CYAN}PowerView (AD reconnaissance):{Colors.NC}")
    print(f"  Import-Module .\\PowerView.ps1")
    print(f"  Get-DomainUser -SPN\n")
    
    print(f"{Colors.GREEN}[+] AD tools preparation complete{Colors.NC}")
    print(f"{Colors.CYAN}Tools location: {tools_dir}{Colors.NC}\n")
    
    return downloaded


def list_ad_tools():
    """
    List all available AD tools and their download status.
    
    Returns:
        dict: Tool status information
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Available AD Tools               ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    status = {}
    
    # Group tools by category
    categories = {
        "BloodHound Collection": ["SharpHound.exe", "SharpHound.ps1"],
        "Kerberos Attacks": ["Rubeus.exe"],
        "Certificate Abuse": ["Certify.exe"],
        "System Enumeration": ["Seatbelt.exe", "SharpUp.exe"],
        "PowerShell Modules": ["PowerView.ps1", "Invoke-Mimikatz.ps1", "ADModule.dll"],
    }
    
    for category, tools in categories.items():
        print(f"{Colors.MAGENTA}{category}:{Colors.NC}")
        for filename in tools:
            if filename in AD_TOOLS:
                dest = tools_dir / filename
                exists = dest.exists()
                
                status[filename] = {
                    "exists": exists,
                    "path": str(dest) if exists else None,
                    "url": AD_TOOLS[filename]
                }
                
                # Display status
                if exists:
                    size = dest.stat().st_size
                    size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"
                    print(f"  {Colors.GREEN}✓{Colors.NC} {filename:<25} ({size_str})")
                else:
                    print(f"  {Colors.RED}✗{Colors.NC} {filename:<25} (not downloaded)")
        print()
    
    print(f"{Colors.CYAN}Tools directory: {tools_dir}{Colors.NC}\n")
    
    return status


def remove_ad_tools():
    """
    Remove all downloaded AD tools.
    
    Returns:
        int: Number of tools removed
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    print(f"\n{Colors.YELLOW}[!] This will remove all Active Directory tools{Colors.NC}")
    print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
    
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return 0
    
    removed = 0
    
    for filename in AD_TOOLS.keys():
        dest = tools_dir / filename
        if dest.exists():
            try:
                dest.unlink()
                print(f"{Colors.GREEN}[+] Removed {filename}{Colors.NC}")
                removed += 1
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to remove {filename}: {e}{Colors.NC}")
    
    if removed > 0:
        print(f"\n{Colors.GREEN}[+] Removed {removed} AD tools{Colors.NC}")
    else:
        print(f"\n{Colors.YELLOW}[*] No AD tools found to remove{Colors.NC}")
    
    return removed