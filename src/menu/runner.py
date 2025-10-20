"""
runner.py - Menu execution engine
Handles menu rendering, input, and navigation with ESC support
"""

import os
import sys
import termios
import tty

from ..config import Colors
from ..core.context import load_lab_config
from ..utils import menu_utils

def clear_screen():
    """Clear the terminal screen"""
    os.system("clear" if os.name != "nt" else "cls")


def get_choice(prompt=""):
    """
    Get user input with ESC key support.
    
    Args:
        prompt: The prompt to display
    
    Returns:
        User input string, or "ESC" if escape key pressed, or None if Enter pressed alone
    """
    print(prompt, end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setraw(fd)
        user_input = ""
        
        while True:
            ch = sys.stdin.read(1)
            
            if ch == "\x1b":  # ESC key
                print()
                return "ESC"
            elif ch in ("\r", "\n"):  # Enter
                print()
                break
            elif ch == "\x7f":  # Backspace
                if user_input:
                    user_input = user_input[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                user_input += ch
                sys.stdout.write(ch)
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return user_input.strip() if user_input else None


def render_menu_items(items):
    """
    Render menu items organized by sections.
    
    Args:
        items: Dictionary of sections containing menu items
    """
    for section, section_items in items.items():
        print(f"\n{Colors.CYAN}{section}:{Colors.NC}")
        for key, (desc, _) in section_items.items():
            print(f"  {Colors.GREEN}[{key}]{Colors.NC} {desc}")


def render_navigation(depth):
    """
    Render navigation hints based on menu depth.
    
    Args:
        depth: Current menu depth (0 = main menu)
    """
    if depth > 0:
        print(f"\n{Colors.CYAN}(Press ESC to go back){Colors.NC}")
    else:
        print(f"\n{Colors.CYAN}(Press 'q' to quit){Colors.NC}")
    print()


def find_action(items, choice):
    """
    Find the action associated with a menu choice.
    
    Args:
        items: Dictionary of sections containing menu items
        choice: User's choice string
    
    Returns:
        Tuple of (description, action) or (None, None) if not found
    """
    for section_items in items.values():
        if choice in section_items:
            return section_items[choice]
    return None, None


def execute_action(action, config, header_func, depth):
    """
    Execute a menu action.
    
    Args:
        action: The action to execute (dict for submenu, callable for function, None for back)
        config: Lab configuration
        header_func: Header rendering function
        depth: Current menu depth
    
    Returns:
        Tuple of (should_continue, should_wait_for_enter)
    """
    if isinstance(action, dict):
        # It's a submenu - recurse (don't wait after returning from submenu)
        run_menu(action, header_func=header_func, config=config, depth=depth + 1)
        return True, False  # Continue menu, but don't wait for Enter
    
    elif callable(action):
        # It's a function - execute it and wait for Enter
        clear_screen()
        action(config)
        return True, True  # Continue menu and wait for Enter
    
    elif action is None:
        # Back command
        return False, False  # Return to parent, no wait
    
    return True, False


def run_menu(menu, header_func=None, config=None, depth=0):
    """
    Recursive menu system with ESC back navigation.
    
    Args:
        menu: Menu definition dictionary containing:
            - title: Menu title
            - context: Optional context block to display
            - items: Dictionary of sections with menu items
        header_func: Optional custom header rendering function
        config: Lab configuration (loaded automatically if None)
        depth: Current menu depth (0 = main menu)
    """
    while True:
        # Always reload config on each iteration to get fresh data
        config = load_lab_config()
        
        clear_screen()
        
        # Get menu components
        title = menu.get("title", "Menu")
        if callable(title):
            title = title(config)
        items = menu.get("items", {})
        context_block = menu.get("context")
        
        # Render header
        if callable(header_func) and depth == 0:
            # Use custom header for main menu
            header_func(config, title)
        else:
            # Use simple header for submenus
            menu_utils.print_title(title, "BLUE")

        # Render context block if present
        if context_block or (depth == 0):
            from .context import render_context
            
            # For main menu, dynamically build context blocks
            if depth == 0:
                from .definitions import build_main_menu_context
                context_blocks = build_main_menu_context(config)
                for block in context_blocks:
                    render_context(block, config)
            elif context_block:
                render_context(context_block, config)
        
        # Render menu items
        render_menu_items(items)
        
        # Render navigation hints
        render_navigation(depth)
        
        # Get user choice
        choice = get_choice(f"{Colors.YELLOW}> {Colors.NC}")
        
        # Handle ESC key
        if choice == "ESC":
            if depth > 0:
                # Return to parent menu
                return
            else:
                # At main menu, ESC does nothing (stay in menu)
                continue
        
        # Handle empty input
        if not choice:
            continue
        
        # Handle quit command - only at main menu (depth 0)
        if choice.lower() == "q":
            if depth == 0:
                print(f"\n{Colors.GREEN}[+] Exiting LabCmdr...{Colors.NC}")
                sys.exit(0)
            else:
                # 'q' in submenu is invalid
                print(f"\n{Colors.YELLOW}[!] Use ESC to go back (or 'q' from main menu to quit){Colors.NC}")
                print(f"{Colors.CYAN}Press Enter to continue...{Colors.NC}", end="")
                input()
                continue
        
        # Find and execute action
        desc, action = find_action(items, choice)
        
        if action is not None or desc is not None:
            should_continue, should_wait = execute_action(action, config, header_func, depth)
            
            if not should_continue:
                # Action returned False, go back to parent menu
                return
            
            # Only wait for Enter if the action requests it
            if should_wait:
                print(f"\n{Colors.CYAN}Press Enter to continue...{Colors.NC}", end="")
                input()
        else:
            # Invalid choice
            print(f"\n{Colors.RED}[!] Invalid choice: {choice}{Colors.NC}")
            print(f"{Colors.CYAN}Press Enter to continue...{Colors.NC}", end="")
            input()