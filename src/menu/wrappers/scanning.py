from datetime import datetime

from ...config import Colors
from ...core.context import (
    load_lab_config,
    find_lab_root,
)

def wrap_run_initial_scan(config):
    """Run initial nmap scan"""
    print(f"\n{Colors.YELLOW}[*] Initial scan not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will run quick nmap scan{Colors.NC}")


def wrap_run_full_scan(config):
    """Run full nmap scan"""
    print(f"\n{Colors.YELLOW}[*] Full scan not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will run comprehensive nmap scan{Colors.NC}")


def wrap_run_udp_scan(config):
    """Run UDP scan"""
    print(f"\n{Colors.YELLOW}[*] UDP scan not implemented yet{Colors.NC}")
    print(f"{Colors.CYAN}Coming soon: Will run UDP port scan{Colors.NC}")


def wrap_view_scan_results(config):
    """View scan results"""
    lab_root = find_lab_root()
    scan_dir = lab_root / "scans" / "nmap"
    
    if not scan_dir.exists() or not any(scan_dir.glob("*.txt")):
        print(f"\n{Colors.YELLOW}[!] No scan results found{Colors.NC}")
        return
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║         Recent Scans                     ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    scans = sorted(scan_dir.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    for i, scan in enumerate(scans[:10], 1):
        size = scan.stat().st_size
        mtime = scan.stat().st_mtime
        time_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        
        print(f"  {Colors.GREEN}[{i}]{Colors.NC} {scan.name}")
        print(f"      {Colors.YELLOW}{time_str} • {size} bytes{Colors.NC}")

__all__ = [
    "wrap_run_initial_scan",
    "wrap_run_full_scan",
    "wrap_run_udp_scan",
    "wrap_view_scan_results",
]