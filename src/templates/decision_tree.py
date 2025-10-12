from ..core.config_manager import get_htb_season
from datetime import datetime

DECISION_TREE = {
    "root": {
        "prompt": "What type of lab?",
        "choices": {
            "1": {"label": "HTB Season", "next": "htb_season", "value": "htb_season"},
            "2": {"label": "Training Platform", "next": "training_platform", "value": "training_platform"},
            "3": {"label": "Conference CTF", "next": "conference_ctf", "value": "conference_ctf"},
            "4": {"label": "Custom", "next": "custom", "value": "custom"}
        }
    },

    "htb_season": {
        "prompts": [
            {"key": "season", "type": "int", "default": get_htb_season(), "prompt": "Season number"},
            {"key": "week", "type": "int", "prompt": "Week number (1-13)", "validate": lambda x: 1 <= int(x) <= 13},
            {"key": "machine_name", "prompt": "Machine name"},
            {"key": "ip_address", "type": "ip", "prompt": "Target IP address", "optional": True},
{"key": "has_credentials", "prompt": "Were you given initial credentials", "choices": {
    "y": {"label": "Yes", "value": "yes"},
    "n": {"label": "No", "value": "no"}
}, "default": "n"},
            {"key": "username", "prompt": "Username", "when": {"has_credentials": "yes"}},
            {"key": "password", "prompt": "Password", "when": {"has_credentials": "yes"}}
        ],
        "path_template": "HTB_Season_{season}/Week{week:02d}-{machine_name}",
        "config": {"platform": "htb", "type": "season"}
    },

    "training_platform": {
        "prompts": [
            {"key": "platform", "prompt": "Platform", "choices": {
                "1": {"label": "Hack The Box (Active/Retired)", "value": "HTB_Active"},
                "2": {"label": "TryHackMe", "value": "THM"},
                "3": {"label": "OffSec Proving Grounds", "value": "OffSec"},
                "4": {"label": "VulnHub", "value": "VulnHub"},
                "5": {"label": "Other", "value": "custom"}
            }},
            {"key": "custom_platform", "prompt": "Platform name", "when": {"platform": "custom"}},
            {"key": "machine_name", "prompt": "Machine/Room name"},
            {"key": "ip_address", "type": "ip", "prompt": "Target IP address", "optional": True},
{"key": "has_credentials", "prompt": "Were you given initial credentials", "choices": {
    "y": {"label": "Yes", "value": "yes"},
    "n": {"label": "No", "value": "no"}
}, "default": "n"},
            {"key": "username", "prompt": "Username", "when": {"has_credentials": "yes"}},
            {"key": "password", "prompt": "Password", "when": {"has_credentials": "yes"}}
        ],
        "path_builder": "build_training_path",
        "config": {"type": "training"}
    },

    "conference_ctf": {
        "prompts": [
            {"key": "conference", "prompt": "Conference", "choices": {
                "1": {"label": "BSides", "value": "bsides"},
                "2": {"label": "DefCon", "value": "defcon"},
                "3": {"label": "Other", "value": "other"}
            }},
            {"key": "conference_name", "prompt": "Conference name", "when": {"conference": "other"}},
            {"key": "village", "prompt": "Village name", "when": {"conference": "defcon"}},
            {"key": "location", "prompt": "Location (e.g., St Pete, Tampa)", "when": {"conference": "bsides"}},
            {"key": "year", "type": "int", "prompt": "Year", "default": datetime.now().year},
            {"key": "challenge_name", "prompt": "Challenge/Lab name", "optional": True},
{"key": "has_credentials", "prompt": "Were you given initial credentials", "choices": {
    "y": {"label": "Yes", "value": "yes"},
    "n": {"label": "No", "value": "no"}
}, "default": "n"},
            {"key": "username", "prompt": "Username", "when": {"has_credentials": "yes"}},
            {"key": "password", "prompt": "Password", "when": {"has_credentials": "yes"}}
        ],
        "path_builder": "build_conference_path",
        "config": {"type": "conference"}
    },

    "custom": {
        "prompts": [
            {"key": "lab_name", "prompt": "Lab name"},
            {"key": "category", "prompt": "Category (optional)", "optional": True},
            {"key": "ip_address", "type": "ip", "prompt": "Target IP address", "optional": True},
{"key": "has_credentials", "prompt": "Were you given initial credentials", "choices": {
    "y": {"label": "Yes", "value": "yes"},
    "n": {"label": "No", "value": "no"}
}, "default": "n"},
            {"key": "username", "prompt": "Username", "when": {"has_credentials": "yes"}},
            {"key": "password", "prompt": "Password", "when": {"has_credentials": "yes"}}
        ],
        "path_builder": "build_custom_path",
        "config": {"type": "custom"}
    }
}