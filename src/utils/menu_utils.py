from ..config import Colors


def print_title(title, titlecolor):
    title_line = title.center(42)
    print(titlecolor)
    print_color= getattr(Colors,titlecolor,None)
    print(f"\n{print_color}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{print_color}║{title_line}║{Colors.NC}")
    print(f"{print_color}╚══════════════════════════════════════════╝{Colors.NC}")


def print_context():
    pass