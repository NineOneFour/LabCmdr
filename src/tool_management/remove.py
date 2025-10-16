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

def remove_tools(toolset):
    """
    Remove all downloaded AD tools.
    
    Returns:
        int: Number of tools removed
    """

    if toolset == "windows":
        tools_dict = WINDOWS_TOOLS
        tool_type = "Windows"
    elif toolset == "linux":
        tools_dict = LINUX_TOOLS
        tool_type = "Linux"
    elif toolset == "ad":
        tools_dict = AD_TOOLS
        tool_type = "AD"
    elif toolset == "all":
        tools_dict = {**WINDOWS_TOOLS, **LINUX_TOOLS, **AD_TOOLS}
        tool_type = "all"
    else:
        print(f"{Colors.RED}[!] Unknown toolset: {toolset}{Colors.NC}")
        return []

    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"
    
    print(f"\n{Colors.YELLOW}[!] This will remove {tool_type} downloaded tools{Colors.NC}")
    print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
    
    if input().strip().lower() != 'y':
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        return 0
    
    removed = 0
    
    for filename in tools_dict.keys():
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