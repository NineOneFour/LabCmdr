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

TOOL_PATH = find_lab_root() / "server" / "serve" / "tools"

def list_tools(toolset):
    """
    List all available AD tools and their download status.
    
    Returns:
        dict: Tool status information
    """
    lab_root = find_lab_root()
    tools_dir = lab_root / "server" / "serve" / "tools"

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
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         {tool_type}               ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    status = {}
    
    for filename,url in tools_dict:
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

