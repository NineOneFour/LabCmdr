"""
decision_tree.py - Flexible decision tree engine for lab path building
"""

from ipaddress import ip_address, IPv4Address
import re
from datetime import datetime
from pathlib import Path
from ..config import Colors
from ..templates.decision_tree import DECISION_TREE
from ..core.copy_files import copy_files
from ..core.config_manager import get_labs_root

# Base path for all labs
def get_base_path():
    """Get labs root from config"""
    return Path(get_labs_root())



# -------- Validation and Type Conversion ----------

def is_valid_ip(s: str) -> bool:
    """Validate IPv4 address"""
    try:
        return isinstance(ip_address(s), IPv4Address)
    except Exception:
        return False

def convert_type(val: str, t: str):
    """Convert string input to specified type"""
    if t == "int":
        return int(val)
    if t == "ip":
        if not is_valid_ip(val):
            raise ValueError("Invalid IP address")
        return val
    return val

def validate_input(val: str, prompt: dict):
    """Validate input against prompt rules"""
    if "validate" in prompt:
        try:
            if not prompt["validate"](val):
                return False, "Value out of range"
        except Exception as e:
            return False, str(e)
    return True, None

# -------- Helper Functions ----------

def should_ask(prompt: dict, ctx: dict) -> bool:
    """Check if a prompt should be asked based on conditions"""
    cond = prompt.get("when")
    if not cond:
        return True
    return all(ctx.get(k) == v for k, v in cond.items())

def clean_name(value: str) -> str:
    """Remove punctuation and whitespace from a string"""
    cleaned = re.sub(r'[^\w\s]', '', value)
    cleaned = re.sub(r'\s+', '', cleaned)
    return cleaned

def clean_location(value: str) -> str:
    """Clean location name and append year"""
    parts = re.findall(r"[A-Za-z0-9]+", value)
    name = "".join(part.capitalize() for part in parts)
    year = datetime.now().year
    return f"{name}{year}"

# -------- User Input Functions ----------

def ask_choice(prompt_text: str, choices: dict, default=None):
    """Present a choice menu and get user selection"""
    print(f"\n{Colors.CYAN}{prompt_text}{Colors.NC}")
    for key, obj in choices.items():
        print(f"  {Colors.GREEN}[{key}]{Colors.NC} {obj['label']}")
    
    # Show default in prompt if provided
    prompt_suffix = f" [{default}]" if default else ""
    
    while True:
        sel = input(f"\n{Colors.YELLOW}Choice{prompt_suffix}: {Colors.NC}").strip()
        
        # Use default if empty and default exists
        if sel == "" and default:
            sel = default
        
        if sel in choices:
            chosen = choices[sel]
            return chosen.get("value", chosen.get("label")), chosen
        print(f"{Colors.RED}Invalid selection, try again.{Colors.NC}")

def ask_free(prompt: dict, context: dict):
    """Get free-form text input from user"""
    label = prompt.get("prompt", prompt["key"].replace("_", " ").title())
    
    # Clean up common abbreviations
    label = (label.replace("Ip ", "IP ")
                 .replace(" Id", " ID")
                 .replace(" Url", " URL"))
    
    default = prompt.get("default")
    optional = prompt.get("optional", False)
    
    while True:
        prompt_text = f"{Colors.CYAN}{label}{Colors.NC}"
        if default is not None:
            prompt_text += f" [{default}]"
        if optional:
            prompt_text += " (optional)"
        
        raw = input(f"{prompt_text}: ").strip()
        
        # Handle optional fields
        if raw == "" and optional:
            return None
        
        # Use default if available
        if raw == "" and default is not None:
            return default
        
        # Don't allow empty non-optional fields
        if raw == "" and not optional:
            print(f"{Colors.RED}This field is required.{Colors.NC}")
            continue
        
        # Type conversion and validation
        try:
            if "type" in prompt:
                val = convert_type(raw, prompt["type"])
            else:
                val = raw
            
            # Additional validation
            valid, error = validate_input(val, prompt)
            if not valid:
                print(f"{Colors.RED}{error}{Colors.NC}")
                continue
            
            return val
            
        except ValueError as e:
            print(f"{Colors.RED}Invalid value: {e}. Try again.{Colors.NC}")

# -------- Path Building Functions ----------

def build_training_path(ctx: dict) -> Path:
    """Build path for training platform labs"""
    platform = ctx.get("custom_platform") if ctx.get("platform") == "custom" else ctx.get("platform")
    machine = ctx.get("machine_name", "unknown")
    return get_base_path() / platform / machine

def build_conference_path(ctx: dict) -> Path:
    """Build path for conference CTF labs"""
    conf = ctx.get("conference", "").lower()
    year = ctx.get("year", datetime.now().year)
    
    if conf == "bsides":
        location = clean_location(ctx.get("location", "Unknown"))
        base = get_base_path() / "BSides" / location
    elif conf == "defcon":
        village = clean_name(ctx.get("village", ""))
        base = get_base_path() / "DefCon" / str(year) / village if village else get_base_path() / "DefCon" / str(year)
    else:
        conf_name = ctx.get("conference_name", "Conference")
        base = get_base_path() / conf_name / str(year)
    
    # Add challenge name if provided
    challenge = ctx.get("challenge_name")
    if challenge:
        return base / challenge
    return base

def build_custom_path(ctx: dict) -> Path:
    """Build path for custom labs"""
    lab_name = ctx.get("lab_name", "CustomLab")
    category = ctx.get("category")
    
    if category:
        return get_base_path() / category / lab_name
    return get_base_path() / lab_name

def build_path(ctx: dict) -> Path:
    """Generate final lab path based on context"""
    root = ctx.get("selected_root")
    
    # HTB Season has its own template
    if root == "htb_season" and "path_template" in DECISION_TREE[root]:
        path_str = DECISION_TREE[root]["path_template"].format(**ctx)
        return get_base_path() / path_str
    
    # Use custom path builder if specified
    node = DECISION_TREE.get(root)
    if node and "path_builder" in node:
        builder_func = globals().get(node["path_builder"])
        if builder_func:
            return builder_func(ctx)
    
    # Fallback
    return get_base_path() / "Uncategorized" / ctx.get("lab_name", f"Lab_{datetime.now().strftime('%Y%m%d')}")

# -------- Main Traversal Function ----------

def traverse(tree=None, node="root", context=None):
    """Traverse the decision tree and collect user input"""
    if tree is None:
        tree = DECISION_TREE
    
    if context is None:
        context = {}
    
    current = tree.get(node)
    if not current:
        return context
    
    # Handle root-level choice menu
    if "choices" in current and "prompt" in current:
        val, chosen = ask_choice(current["prompt"], current["choices"])
        context["selected_root"] = val
        next_node = chosen.get("next")
        if next_node:
            return traverse(tree, next_node, context)
        return context
    
    # Process prompt list
    for prompt in current.get("prompts", []):
        if not should_ask(prompt, context):
            continue
        
        key = prompt["key"]
        
        # Choice-type prompt
        if "choices" in prompt:
            prompt_text = prompt.get("prompt", key.replace("_", " ").title())
            default = prompt.get("default") 
            val, chosen = ask_choice(prompt_text, prompt["choices"], default)
            context[key] = val
            if chosen.get("next"):
                traverse(tree, chosen["next"], context)
            continue
        
        # Free-text prompt
        val = ask_free(prompt, context)
        if val is not None:  # Don't add None values for optional fields
            context[key] = val
    
    # Apply configuration
    if "config" in current:
        context.update(current["config"])
    
    return context

# -------- Public Interface ----------

def create_lab(path=None):
    """
    Create a new lab structure.
    
    Args:
        path: Optional direct path. If None, use interactive mode.
    
    Returns:
        Path object for the lab directory
    """
    from ..core.builder import create_structure, save_context
    from ..core.copy_files import copy_files 
    
    if path:
        # Direct path mode
        lab_path = Path(path).expanduser().resolve()
        context = {}
    else:
        # Interactive mode
        print(f"\n{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.BLUE}║         Lab Type Selection               ║{Colors.NC}")
        print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.NC}")
        
        # Traverse the decision tree
        context = traverse()
        
        # Build the final path
        lab_path = build_path(context)
        
        # Store metadata in context
        context["full_path"] = str(lab_path)
    
    # Create the structure
    print(f"\n{Colors.CYAN}[*] Creating lab at: {lab_path}{Colors.NC}\n")
    print(f"{Colors.YELLOW}[*] Creating folder structure...{Colors.NC}")
    overwrite_mode = create_structure(str(lab_path))  # CAPTURE the return value
    print(f"{Colors.GREEN}[+] Folder structure created{Colors.NC}\n")

    print(f"{Colors.YELLOW}[*] Copying template files...{Colors.NC}")
    copy_files(str(lab_path), overwrite_mode=overwrite_mode)  # PASS it along
    print(f"{Colors.GREEN}[+] Template files copied{Colors.NC}\n")    
    
    # Save config
    if context:
        save_context(context, lab_path)
        print(f"{Colors.GREEN}[+] Saved config to labcmdr/labconfig.json{Colors.NC}\n")
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.GREEN}║  Lab created successfully!               ║{Colors.NC}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.CYAN}Next steps:{Colors.NC}")
    print(f"  1. cd {lab_path}")
    print(f"  2. labcmdr start")
    print(f"  3. Start hacking! 🚀\n")
    
    return lab_path