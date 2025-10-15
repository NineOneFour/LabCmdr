import sys
from ...actions.download_lin import (
    download_linux_tools,
    list_linux_tools,
    remove_linux_tools,
)
from ...actions.download_win import (
    download_windows_tools,
    list_windows_tools,
    remove_windows_tools,
)
from ...actions.download_ad import (
    download_ad_tools,
    list_ad_tools,
    remove_ad_tools,
)
from ...config import Colors


def wrap_download_linux_tools(config):
    """Download Linux tools"""
    print(f"\n{Colors.CYAN}[*] Downloading Linux enumeration tools...{Colors.NC}")
    
    # Ask if user wants to force re-download
    print(f"\n{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        download_linux_tools(force=force)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading Linux tools: {e}{Colors.NC}")


def wrap_download_windows_tools(config):
    """Download Windows tools"""
    print(f"\n{Colors.CYAN}[*] Downloading Windows enumeration tools...{Colors.NC}")
    
    # Ask if user wants to force re-download
    print(f"\n{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        download_windows_tools(force=force)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading Windows tools: {e}{Colors.NC}")


def wrap_download_ad_tools(config):
    """Download AD tools"""
    print(f"\n{Colors.CYAN}[*] Downloading Active Directory enumeration tools...{Colors.NC}")
    
    # Ask if user wants to force re-download
    print(f"\n{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        download_ad_tools(force=force)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading AD tools: {e}{Colors.NC}")


def wrap_download_all_tools(config):
    """Download all tools"""
    print(f"\n{Colors.CYAN}[*] Downloading ALL enumeration tools...{Colors.NC}")
    print(f"{Colors.YELLOW}[*] This will download Linux, Windows, and AD tools{Colors.NC}\n")
    
    # Ask if user wants to force re-download
    print(f"{Colors.YELLOW}Re-download existing files? (y/n):{Colors.NC} ", end="")
    force = input().strip().lower() == 'y'
    
    try:
        print(f"\n{Colors.BLUE}[1/3] Linux Tools{Colors.NC}")
        download_linux_tools(force=force)
        
        print(f"\n{Colors.BLUE}[2/3] Windows Tools{Colors.NC}")
        download_windows_tools(force=force)
        
        print(f"\n{Colors.BLUE}[3/3] Active Directory Tools{Colors.NC}")
        download_ad_tools(force=force)
        
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.GREEN}║     All Tools Downloaded!                ║{Colors.NC}")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════╝{Colors.NC}")
        
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading tools: {e}{Colors.NC}")


def wrap_list_tools(config):
    """List available tools"""
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║         Tool Status Overview             ║{Colors.NC}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}")
    
    try:
        # Show all three categories
        list_linux_tools()
        list_windows_tools()
        list_ad_tools()
        
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error listing tools: {e}{Colors.NC}")


def wrap_remove_tools_menu(config):
    """Show submenu for removing tools"""
    print(f"\n{Colors.CYAN}Remove which tools?{Colors.NC}")
    print(f"  {Colors.GREEN}[1]{Colors.NC} Linux tools")
    print(f"  {Colors.GREEN}[2]{Colors.NC} Windows tools")
    print(f"  {Colors.GREEN}[3]{Colors.NC} AD tools")
    print(f"  {Colors.GREEN}[4]{Colors.NC} All tools")
    print(f"  {Colors.GREEN}[c]{Colors.NC} Cancel")
    
    choice = input(f"\n{Colors.YELLOW}Choice: {Colors.NC}").strip().lower()
    
    try:
        if choice == '1':
            remove_linux_tools()
        elif choice == '2':
            remove_windows_tools()
        elif choice == '3':
            remove_ad_tools()
        elif choice == '4':
            print(f"\n{Colors.RED}[!] WARNING: This will remove ALL tools{Colors.NC}")
            print(f"{Colors.YELLOW}Continue? (y/n):{Colors.NC} ", end="")
            if input().strip().lower() == 'y':
                total = 0
                total += remove_linux_tools()
                total += remove_windows_tools()
                total += remove_ad_tools()
                print(f"\n{Colors.GREEN}[+] Removed {total} total tools{Colors.NC}")
        elif choice == 'c':
            print(f"{Colors.YELLOW}[*] Cancelled{Colors.NC}")
        else:
            print(f"{Colors.RED}[!] Invalid choice{Colors.NC}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error removing tools: {e}{Colors.NC}")


__all__ = [
    "wrap_download_linux_tools",
    "wrap_download_windows_tools",
    "wrap_download_ad_tools",
    "wrap_download_all_tools",
    "wrap_list_tools",
    "wrap_remove_tools_menu",
]