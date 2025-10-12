#!/usr/bin/env python3
"""
run.py - Interactive lab control panel
Uses the menu package for a clean, modular interface
"""

import sys
import subprocess
from ..menu import run_menu, MAIN_MENU
from ..menu.context import main_header
from ..core.context import LabNotFoundError, find_lab_root
from ..config import Colors


def check_vpn_connection():
    """
    Check if tun0 interface exists (VPN connected).
    
    Returns:
        tuple: (bool: is_connected, str: ip_address or None)
    """
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", "tun0"],
            capture_output=True,
            text=True,
            check=True
        )
        # If command succeeds, tun0 exists
        for line in result.stdout.split('\n'):
            if 'inet ' in line:
                ip = line.strip().split()[1].split('/')[0]
                return True, ip
        return True, None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None


def display_vpn_warning():
    """Display warning about missing VPN connection"""
    print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.YELLOW}║         VPN WARNING                      ║{Colors.NC}")
    print(f"{Colors.YELLOW}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.RED}[!] No VPN connection detected (tun0 not found){Colors.NC}\n")
    
    print(f"{Colors.CYAN}Impact:{Colors.NC}")
    print(f"  • HTTP server will not start without tun0")
    print(f"  • Cannot determine your attack machine IP")
    print(f"  • Target may not be reachable\n")
    
    print(f"{Colors.CYAN}To connect:{Colors.NC}")
    print(f"  sudo openvpn --config /path/to/your.ovpn\n")
    
    print(f"{Colors.YELLOW}You can still use labcmdr for:{Colors.NC}")
    print(f"  • Configuration management")
    print(f"  • Note taking")
    print(f"  • Tool downloads")
    print(f"  • Viewing scan results\n")


def main_menu():
    """
    Entry point for the interactive lab control panel.
    Automatically detects lab context and launches menu.
    """
    try:
        # Verify we're in a lab directory
        lab_root = find_lab_root()
        
        # Check VPN connection
        vpn_connected, vpn_ip = check_vpn_connection()
        
        # Sanity check: does labcmdr directory exist?
        from pathlib import Path
        labcmdr_dir = lab_root / "labcmdr"
        config_file = labcmdr_dir / "labconfig.json"
        
        if not labcmdr_dir.exists() or not config_file.exists():
            print(f"\n{Colors.YELLOW}[!] Warning: This doesn't look like a complete lab directory{Colors.NC}")
            print(f"{Colors.CYAN}Location: {lab_root}{Colors.NC}")
            
            if not labcmdr_dir.exists():
                print(f"\n{Colors.RED}Missing: labcmdr/ directory{Colors.NC}")
            elif not config_file.exists():
                print(f"\n{Colors.RED}Missing: labcmdr/labconfig.json{Colors.NC}")
            
            print(f"\n{Colors.CYAN}This directory was likely not created with 'labcmdr create'.{Colors.NC}")
            print(f"{Colors.YELLOW}Would you like to initialize it as a lab? (y/n):{Colors.NC} ", end="")
            
            response = input().strip().lower()
            
            if response == 'y':
                # Create minimal structure
                from ..core.builder import save_context
                from datetime import datetime
                
                # Create labcmdr directory
                labcmdr_dir.mkdir(exist_ok=True)
                
                # Create minimal context
                minimal_context = {
                    'lab_name': lab_root.name,
                    'type': 'manual',
                    'platform': 'unknown'
                }
                
                save_context(minimal_context, lab_root)
                
                print(f"\n{Colors.GREEN}[+] Initialized lab directory{Colors.NC}")
                print(f"{Colors.CYAN}[*] You can update the configuration from the menu{Colors.NC}")
                print(f"\n{Colors.CYAN}Press Enter to continue...{Colors.NC}", end="")
                input()
            else:
                print(f"\n{Colors.YELLOW}[*] Cancelled{Colors.NC}")
                sys.exit(0)
        
        # Display VPN warning if not connected
        if not vpn_connected:
            display_vpn_warning()
            print(f"{Colors.YELLOW}Continue anyway? (y/n):{Colors.NC} ", end="")
            response = input().strip().lower()
            
            if response != 'y':
                print(f"\n{Colors.CYAN}[*] Exiting - Connect to VPN and try again{Colors.NC}")
                sys.exit(0)
        else:
            # VPN connected - show success message
            print(f"\n{Colors.GREEN}[✓] VPN Connected: {vpn_ip}{Colors.NC}")
        
        # Run the main menu with custom header
        run_menu(MAIN_MENU, header_func=main_header, depth=0)
        
    except LabNotFoundError as e:
        print(f"\n{Colors.RED}[!] {e}{Colors.NC}")
        print(f"\n{Colors.CYAN}You can create a new lab with:{Colors.NC}")
        print(f"  labcmdr create")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[*] Interrupted by user{Colors.NC}")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n{Colors.RED}[!] Unexpected error: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main_menu()