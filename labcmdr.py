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
from src.commands.help import show_help  # NEW IMPORT


def main():
    # Check for help flag BEFORE argparse (to show custom help)
    if len(sys.argv) > 1 and sys.argv[1] in ['help', '--help', '-h']:
        show_help()
        sys.exit(0)
    
    parser = argparse.ArgumentParser(
        description='Lab environment management tool for CTF/Pentesting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,  # Disable default help (we have custom)
        epilog="""
Commands:
  create      Create a new lab environment
  run         Interactive lab control panel
  status      Show lab status
  config      Manage configuration
  help        Show detailed help
  
Examples:
  labcmdr create              # Interactive lab creation
  labcmdr run                 # Start lab control panel
  labcmdr help                # Show detailed help
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['create', 'run', 'status', 'config', 'help'],
        help='Command to run'
    )
    
    # Additional positional args (context-dependent)
    parser.add_argument(
        'subcommand',
        nargs='?',
        help='Subcommand (e.g., config subcommands)'
    )
    
    parser.add_argument(
        'arg1',
        nargs='?',
        help='First argument'
    )
    
    parser.add_argument(
        'arg2',
        nargs='?',
        help='Second argument'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='labcmdr 1.0.0'
    )
    
    # Custom help flag
    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help message'
    )
    
    args = parser.parse_args()
    
    # Handle help command
    if args.command == 'help' or args.help:
        show_help()
        sys.exit(0)
    
    # Default to create if no command given
    if not args.command:
        args.command = 'create'
    
    try:
        if args.command == 'create':
            from src.commands.create import create_lab
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