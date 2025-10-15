from ...config import Colors
from ...actions.update_lab import edit_field

def wrap_edit_metadata_field(config):
    """Wrapper for editing metadata fields"""
    print(f"\n{Colors.CYAN}Available metadata fields:{Colors.NC}")
    print(f"  name, platform, season, week, year, conference, location, etc.")
    
    field = input(f"\n{Colors.YELLOW}Enter field name to edit: {Colors.NC}").strip()
    
    if field:
        edit_field("metadata", field)
    else:
        print(f"{Colors.RED}[!] No field specified{Colors.NC}")


def wrap_edit_network_field(config):
    """Wrapper for editing network fields"""
    print(f"\n{Colors.CYAN}Available network fields:{Colors.NC}")
    print(f"  ip_address, domain, domain_name, domain_controller")
    
    field = input(f"\n{Colors.YELLOW}Enter field name to edit: {Colors.NC}").strip()
    
    if field:
        edit_field("network", field)
    else:
        print(f"{Colors.RED}[!] No field specified{Colors.NC}")


def wrap_edit_credentials_field(config):
    """Wrapper for editing credential fields"""
    print(f"\n{Colors.CYAN}Available credential fields:{Colors.NC}")
    print(f"  username, password")
    
    field = input(f"\n{Colors.YELLOW}Enter field name to edit: {Colors.NC}").strip()
    
    if field:
        edit_field("credentials", field)
    else:
        print(f"{Colors.RED}[!] No field specified{Colors.NC}")

__all__ = [
    "wrap_edit_metadata_field",
    "wrap_edit_network_field",
    "wrap_edit_credentials_field",
]