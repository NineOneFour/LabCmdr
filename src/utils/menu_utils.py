# from ..config import Colors

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # No Color

def print_title(title, titlecolor):
    title_line = title.center(42)
    print(titlecolor)
    print_color= getattr(Colors,titlecolor,None)
    print(f"\n{print_color}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{print_color}║{title_line}║{Colors.NC}")
    print(f"{print_color}╚══════════════════════════════════════════╝{Colors.NC}")


