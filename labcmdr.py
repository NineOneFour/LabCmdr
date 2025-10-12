#!/usr/bin/env python3
"""
labcmdr - Lab environment management tool
Entry point for the command-line interface
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Colors
from src.core.context import LabNotFoundError


def main():
    parser = argparse.ArgumentParser(
        description='Lab environment management tool for CTF/Pentesting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  create      Create a new lab environment
  start       Start lab (scans + server)
  server      Start HTTP server
  manage      Interactive configuration management
  status      Show lab status
  
Examples:
  labcmdr create              # Interactive lab creation
  labcmdr create /path/to/lab # Create at specific path
  labcmdr start               # Start current lab (scans + server)
  labcmdr server              # Start server only
  labcmdr manage              # Update config interactively
  labcmdr status              # Show current lab info
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['create', 'run', 'status'],  # Simplified
        help='Command to run'
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        help='Path for lab creation (only used with create command)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='labcmdr 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Default to create if no command given
    if not args.command:
        args.command = 'create'
    
    try:
        if args.command == 'create':
            from src.commands.create import create_lab
            create_lab(args.path)

        elif args.command == 'run':
            from src.commands.run import main_menu
            main_menu()
                
        elif args.command == 'start':
            print(f"{Colors.YELLOW}[*] 'start' command not implemented yet{Colors.NC}")
            print(f"{Colors.CYAN}Coming soon: Will run initial scans and start server{Colors.NC}")
        
        elif args.command == 'server':
            print(f"{Colors.YELLOW}[*] 'server' command not implemented yet{Colors.NC}")
            print(f"{Colors.CYAN}Coming soon: Will start HTTP server for current lab{Colors.NC}")
        
        elif args.command == 'manage':
            print(f"{Colors.YELLOW}[*] 'manage' command not implemented yet{Colors.NC}")
            print(f"{Colors.CYAN}Coming soon: Interactive config management{Colors.NC}")
        
        elif args.command == 'status':
            from src.core.context import find_lab_root, load_lab_config
            lab_root = find_lab_root()
            config = load_lab_config(lab_root)
            
            print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
            print(f"{Colors.CYAN}║         Lab Status                       ║{Colors.NC}")
            print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
            
            print(f"{Colors.GREEN}Lab:{Colors.NC} {config['metadata']['name']}")
            print(f"{Colors.GREEN}Location:{Colors.NC} {lab_root}")
            print(f"{Colors.GREEN}Platform:{Colors.NC} {config['metadata']['platform']}")
            print(f"{Colors.GREEN}Type:{Colors.NC} {config['metadata']['type']}")
            
            if config['network']['ip_address']:
                print(f"{Colors.GREEN}Target IP:{Colors.NC} {config['network']['ip_address']}")
            
            if config['credentials']['username']:
                print(f"{Colors.GREEN}Username:{Colors.NC} {config['credentials']['username']}")
            
            print()
        
        elif args.command == 'stop':
            print(f"{Colors.YELLOW}[*] 'stop' command not implemented yet{Colors.NC}")
            print(f"{Colors.CYAN}Coming soon: Will stop running server{Colors.NC}")
    
    except LabNotFoundError as e:
        print(f"\n{Colors.RED}[!] {e}{Colors.NC}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Cancelled by user{Colors.NC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()