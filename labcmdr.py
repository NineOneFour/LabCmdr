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
from src.commands.config import config_cli


def main():
    parser = argparse.ArgumentParser(
        description='Lab environment management tool for CTF/Pentesting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  create      Create a new lab environment
  run         Interactive lab control panel
  status      Show lab status
  config      Manage configuration
  
Examples:
  labcmdr create              # Interactive lab creation
  labcmdr create /path/to/lab # Create at specific path
  labcmdr run                 # Start lab control panel
  labcmdr status              # Show current lab info
  labcmdr config              # Config management menu
  labcmdr config show         # Display configuration
  labcmdr config edit         # Edit config file
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['create', 'run', 'status', 'config'],
        help='Command to run'
    )
    
    # Additional positional args (context-dependent)
    parser.add_argument(
        'subcommand',
        nargs='?',
        help='Subcommand (e.g., config subcommands: show, edit, get, set, init, reset, path, validate)'
    )
    
    parser.add_argument(
        'arg1',
        nargs='?',
        help='First argument (path for create, key for config get/set)'
    )
    
    parser.add_argument(
        'arg2',
        nargs='?',
        help='Second argument (value for config set)'
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
            # arg1 is the path for create command
            create_lab(args.arg1)

        elif args.command == 'run':
            from src.commands.run import main_menu
            main_menu()
        
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
        
        elif args.command == 'config':
            # Map args to what config_cli expects
            args.config_command = args.subcommand
            args.key = args.arg1
            args.value = args.arg2
            config_cli(args)
    
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