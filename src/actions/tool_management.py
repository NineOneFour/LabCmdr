import os
import urllib.request
from pathlib import Path
from ..config import Colors
from ..core.context import find_lab_root

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

LINUX_TOOLS = {
    "linpeas.sh": "https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh",
    "pspy64": "https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64",
    "pspy32": "https://github.com/DominicBreuker/pspy/releases/latest/download/pspy32",
    "linenum.sh": "https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh",
    "lse.sh": "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh",
}

WINDOWS_TOOLS = {
    "winpeas64.exe": "https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASx64.exe",
    "winpeas32.exe": "https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASx86.exe",
    "winpeasany.exe": "https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASany.exe",
    "mimikatz64.exe": "https://github.com/gentilkiwi/mimikatz/releases/latest/download/mimikatz_trunk.zip",
    "nc64.exe": "https://github.com/int0x33/nc.exe/raw/master/nc64.exe",
    "nc32.exe": "https://github.com/int0x33/nc.exe/raw/master/nc.exe",
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
    
def download_tools(toolset, force=False):
    """
    Download all Active Directory enumeration tools to current lab's tools directory.
    These tools are meant to be transferred to and run on target Windows machines.
    
    Args:
        force: If True, re-download even if files exist
    
    Returns:
        list: Paths to downloaded tools
    """

    if toolset == None:
        return []

    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    toolset_info = check_toolset(toolset)
    
    # Create tools directory if it doesn't exist
    tools_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")

    print(f"{Colors.BLUE}║       Downloading {toolset_info["tools"]} Tools               ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.CYAN}[*] These tools run ON target Windows machines{Colors.NC}")
    print(f"{Colors.CYAN}[*] BloodHound GUI should be installed on your attacking machine{Colors.NC}\n")
    
    downloaded = []
    skipped = []
    failed = []
    
    for filename, url in toolset_info["toolset"].items():
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

def list_tools(toolset):
    """
    List all available AD tools and their download status.
    
    Returns:
        dict: Tool status information
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    toolset_info = check_toolset(toolset)
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         {toolset_info["title"]}               ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    status = {}
    
    for filename,url in toolset_info["toolset"].items():
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
            print(f"  {Colors.GREEN}✓{Colors.NC} {filename:<25} ({size_str})")
        else:
            print(f"  {Colors.RED}✗{Colors.NC} {filename:<25}")
    
    print()
    print(f"{Colors.CYAN}Tools directory: {tools_dir}{Colors.NC}\n")
    
    return status

def remove_tools(toolset):
    """
    Remove all downloaded AD tools.
    
    Returns:
        int: Number of tools removed
    """

    if toolset == None:
        return 0
    
    toolset_info = check_toolset(toolset)

    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    print(f"\n{Colors.YELLOW}[!] This will remove {toolset_info["tools"]} downloaded tools{Colors.NC}")
    print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
    
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return 0
    
    removed = 0
    
    for filename in toolset_info["toolset"].keys():
        dest = tools_dir / filename
        if dest.exists():
            try:
                dest.unlink()
                print(f"{Colors.GREEN}[+] Removed {filename}{Colors.NC}")
                removed += 1
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to remove {filename}: {e}{Colors.NC}")
    
    if removed > 0:
        print(f"\n{Colors.GREEN}[+] Removed {removed} tools{Colors.NC}")
    else:
        print(f"\n{Colors.YELLOW}[*] No tools found to remove{Colors.NC}")
    
    return removed

def check_toolset(toolset):
    if toolset == "windows":
        tools_dict = WINDOWS_TOOLS
        title = "Available Windows Tools"
        tools="Windows"
    elif toolset == "linux":
        tools_dict = LINUX_TOOLS
        title = "Available Linux Tools"
        tools="Linux"
    elif toolset == "ad":
        tools_dict = AD_TOOLS
        title = "Available AD Tools"
        tools="AD"
    elif toolset == "all":
        tools_dict = {**WINDOWS_TOOLS, **LINUX_TOOLS, **AD_TOOLS}
        title = "All Available Tools"
        tools="All"
    else:
        print(f"{Colors.RED}[!] Unknown toolset: {toolset}{Colors.NC}")
        return {}
    toolset_return = {
        "toolset": tools_dict,
        "title": title,
        "tools": tools,
    }
    
    return toolset_return