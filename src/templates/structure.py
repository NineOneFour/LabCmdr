STRUCTURE = {
    "notes": {
        "enumeration.md": None,
        "escalation.md": None,
        "general_notes.md": None,
        "initial_access.md": None,
        "walkthrough.md": None
    },
    "server": {
        "serve": {  # Files to serve to target
            "exploits": {},  # Your custom exploits/scripts
            "tools": {},     # Downloaded enumeration tools (linpeas, winpeas, etc.)
            "payloads": {}   # Reverse shells, webshells, etc.
        },
        "loot": {
            "creds": {
                "scratchpad.txt": None,
                "passwords.txt": None,
                "usernames.txt": None
            },
            "interesting_files": {},
            "hashes": {},
            "screenshots": {}  # Maybe add this too?
        }
    },
    "labcmdr":{
        "labconfig.yaml":None,
    },
    "scans": {  # Nice to have nmap/scan outputs separate
        "nmap": {}
    }
}

COPYFILES = {
    "templates/notes/reminders.md": "notes/reminders.md",
    "templates/notes/checklist.md": "notes/checklist.md",
}
