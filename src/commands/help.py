#!/usr/bin/env python3
"""
help.py - Custom help display with ASCII banner and paged output
"""

import subprocess
from ..config import Colors


LABCMDR_BANNER = r"""
.____          ___.   _________              .___       
|    |   _____ \_ |__ \_   ___ \  _____    __| _/______ 
|    |   \__  \ | __ \/    \  \/ /     \  / __ |\_  __ \ 
|    |___ / __ \| \_\ \     \___|  Y Y  \/ /_/ | |  | \/
|_______ (____  /___  /\______  /__|_|  /\____ | |__|   
        \/    \/    \/        \/      \/      \/        
"""


def build_help_content():
    """Build the help content as a string"""
    lines = []
    
    # Banner
    lines.append(f"\n{Colors.CYAN}{LABCMDR_BANNER}{Colors.NC}")
    
    # Tagline
    lines.append(f"{Colors.BLUE}{'=' * 60}{Colors.NC}")
    lines.append(f"{Colors.YELLOW}Lab Environment Management for CTF & Penetration Testing{Colors.NC}")
    lines.append(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")
    
    # Usage section
    lines.append(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    lines.append(f"{Colors.CYAN}║                      USAGE                               ║{Colors.NC}")
    lines.append(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    lines.append(f"  {Colors.GREEN}labcmdr{Colors.NC} {Colors.YELLOW}<command>{Colors.NC} {Colors.MAGENTA}[options]{Colors.NC}\n")
    
    # Commands section
    lines.append(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    lines.append(f"{Colors.CYAN}║                     COMMANDS                             ║{Colors.NC}")
    lines.append(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    commands = [
        ("create", "[path]", "Create a new lab environment"),
        ("run", "", "Launch interactive lab control panel"),
        ("status", "", "Show current lab status and info"),
        ("config", "[subcommand]", "Manage global configuration"),
        ("help", "", "Show this help message"),
    ]
    
    for cmd, args, desc in commands:
        if args:
            lines.append(f"  {Colors.GREEN}{cmd:<12}{Colors.NC} {Colors.MAGENTA}{args:<15}{Colors.NC} {desc}")
        else:
            lines.append(f"  {Colors.GREEN}{cmd:<12}{Colors.NC} {' ' * 15} {desc}")
    
    lines.append("")
    
    # Config subcommands section
    lines.append(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    lines.append(f"{Colors.CYAN}║                CONFIG SUBCOMMANDS                        ║{Colors.NC}")
    lines.append(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    config_cmds = [
        ("show", "", "Display current configuration"),
        ("edit", "", "Open config file in editor"),
        ("get", "<key>", "Get value of config key"),
        ("set", "<key> <value>", "Set value of config key"),
        ("init", "", "Initialize/create config file"),
        ("reset", "", "Reset config to defaults"),
        ("path", "", "Show config file location"),
        ("validate", "", "Validate configuration"),
    ]
    
    lines.append(f"  {Colors.GREEN}labcmdr config{Colors.NC} {Colors.YELLOW}<subcommand>{Colors.NC}\n")
    
    for cmd, args, desc in config_cmds:
        if args:
            lines.append(f"  {Colors.YELLOW}{cmd:<12}{Colors.NC} {Colors.MAGENTA}{args:<15}{Colors.NC} {desc}")
        else:
            lines.append(f"  {Colors.YELLOW}{cmd:<12}{Colors.NC} {' ' * 15} {desc}")
    
    lines.append("")
    
    # Examples section
    lines.append(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    lines.append(f"{Colors.CYAN}║                     EXAMPLES                             ║{Colors.NC}")
    lines.append(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    examples = [
        ("Create a new lab (interactive)", "labcmdr create"),
        ("Create lab at specific path", "labcmdr create ~/Labs/MyLab"),
        ("Start lab control panel", "cd ~/Labs/HTB_Season_9/Week01-BoardLight && labcmdr run"),
        ("Check lab status", "labcmdr status"),
        ("View configuration", "labcmdr config show"),
        ("Edit configuration", "labcmdr config edit"),
        ("Get labs directory", "labcmdr config get paths.labs_root"),
        ("Set default port", "labcmdr config set server.default_port 9000"),
    ]
    
    for desc, cmd in examples:
        lines.append(f"  {Colors.BLUE}#{Colors.NC} {desc}")
        lines.append(f"    {Colors.GREEN}${Colors.NC} {cmd}\n")
    
    # Quick tips section
    lines.append(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    lines.append(f"{Colors.CYAN}║                    QUICK TIPS                            ║{Colors.NC}")
    lines.append(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    tips = [
        "LabCmdr works from anywhere inside a lab directory (like git)",
        "Use 'labcmdr run' for an interactive menu with all features",
        "Config file: ~/.config/labcmdr/config.yaml",
        "Each lab has its own config: <lab>/labcmdr/labconfig.yaml",
        "Press ESC to go back in menus, 'q' to quit from main menu",
    ]
    
    for tip in tips:
        lines.append(f"  {Colors.YELLOW}•{Colors.NC} {tip}")
    
    lines.append("")
    
    # Footer
    lines.append(f"{Colors.BLUE}{'=' * 60}{Colors.NC}")
    lines.append(f"{Colors.GREEN}Ready to hack! {Colors.NC}")
    lines.append(f"{Colors.CYAN}For detailed documentation, visit: https://github.com/yourusername/LabCmdr{Colors.NC}\n")
    lines.append(f"{Colors.CYAN}Press q to quit{Colors.NC}\n")
    return "\n".join(lines)


def show_help():
    """Display the custom help screen with pager"""
    content = build_help_content()
    
    try:
        # Use less with -R to preserve ANSI colors
        # -X prevents clearing screen on exit
        # -F exits immediately if content fits on one screen
        proc = subprocess.Popen(
            ['less', '-RXF'],
            stdin=subprocess.PIPE,
            text=True
        )
        proc.communicate(input=content)
    except (FileNotFoundError, BrokenPipeError):
        # Fallback if less not available or user quits early
        print(content)