"""
definitions.py - Menu structure definitions
Defines all menu hierarchies and their context blocks
"""

from .context import (
    get_lab_name,
    get_target_ip,
    get_server_status,
    get_last_scan,
    get_platform,
    get_fqdn_count,
    get_username,
    get_password,
    has_credentials,
    get_attacker_ip,
    get_main_menu_title
)
from .wrappers import (
    wrap_start_server,
    wrap_stop_server,
    wrap_restart_server,
    wrap_server_status,
    wrap_run_initial_scan,
    wrap_run_full_scan,
    wrap_run_udp_scan,
    wrap_view_scan_results,
    wrap_download_linux_tools,
    wrap_download_windows_tools,
    wrap_download_ad_tools,
    wrap_download_all_tools,
    wrap_list_tools,
    wrap_open_notes,
    wrap_open_scans,
    wrap_show_lab_info,
    wrap_edit_metadata_field,
    wrap_edit_network_field,
    wrap_edit_credentials_field,
    wrap_view_server_log,
    wrap_start_stop_server,
    wrap_quick_commands,
    wrap_change_port,
)

from ..actions.update_lab import (
    quick_ip_update,
    view_config,
    add_fqdn,
    remove_fqdn,
    list_fqdns,
    edit_field,
)

from ..actions.manage_host import (
    update_hosts,
    remove_from_hosts,
    view_hosts_entries,
)


def build_main_menu_context(config):
    """
    Build the main menu context blocks dynamically.
    Returns a list of context blocks to render.
    
    Args:
        config: Lab configuration dictionary
    
    Returns:
        List of context block dictionaries
    """
    contexts = []
    
    # Main status block (always shown)
    contexts.append({
        "title": "Status:",
        "fields": [
            ("Attacker",get_attacker_ip),
            ("Target", get_target_ip),
            ("Server", get_server_status),
        ]
    })
    
    # Credentials block (only if credentials exist)
    if has_credentials(config):
        cred_fields = []
        
        username = get_username(config)
        if username:
            cred_fields.append(("Username", get_username))
        
        password = get_password(config)
        if password:
            cred_fields.append(("Password", get_password))
        
        if cred_fields:
            contexts.append({
                "title": "Creds:",
                "fields": cred_fields
            })
    
    return contexts


# ======================
#   SERVER SUBMENU
# ======================




# ======================
#   SCANNING SUBMENU
# ======================

SCANNING_MENU = {
    "title": "Scanning",
    "context": {
        "title": "",
        "fields": [
            ("Target IP", get_target_ip),
            ("Last Scan", get_last_scan),
        ]
    },
    "items": {
        "Scans": {
            "1": ("Run Initial Scan (quick)", wrap_run_initial_scan),
            "2": ("Run Full TCP Scan", wrap_run_full_scan),
            "3": ("Run UDP Scan", wrap_run_udp_scan),
            "4": ("View Scan Results", wrap_view_scan_results),
        },

    }
}


# ======================
#   TOOLS SUBMENU
# ======================

TOOLS_MENU = {
    "title": "Download Tools",
    "items": {
        "Tool Categories": {
            "1": ("Linux Tools (LinPEAS, pspy, etc.)", wrap_download_linux_tools),
            "2": ("Windows Tools (WinPEAS, Mimikatz, etc.)", wrap_download_windows_tools),
            "3": ("AD Tools (BloodHound, Rubeus, etc.)", wrap_download_ad_tools),
            "4": ("Download All", wrap_download_all_tools),
        },
        "Info": {
            "5": ("List Available Tools", wrap_list_tools),
        },

    }
}


# ======================
#   METADATA EDITOR SUBMENU
# ======================

METADATA_EDITOR_MENU = {
    "title": "Edit Metadata",
    "context": {
        "title": "",
        "fields": [
            ("Lab Name", get_lab_name),
            ("Platform", get_platform),
        ]
    },
    "items": {
        "Fields": {
            "1": ("Edit Name", lambda c: edit_field("metadata", "name")),
            "2": ("Edit Platform", lambda c: edit_field("metadata", "platform")),
            "3": ("Edit Season", lambda c: edit_field("metadata", "season")),
            "4": ("Edit Week", lambda c: edit_field("metadata", "week")),
            "5": ("Edit Year", lambda c: edit_field("metadata", "year")),
        },

    }
}

# ======================
#   SERVER MANAGEMENT SUBMENU
# ======================

SERVER_MANAGEMENT_MENU = {
    "title": "Server Management",
    "context": {
        "title": "",
        "fields": [
            ("Server", get_server_status),
        ]
    },
    "items": {
        "Server": {
            "1": ("Start/Stop Server", wrap_start_stop_server),
            "2": ("Restart Server", wrap_restart_server),
            "3": ("Change Port", wrap_change_port),
        },
        "Utility": {
            "4": ("View Logs", wrap_view_server_log),
            "5": ("Download Tools", TOOLS_MENU),
        }
    }
}


# ======================
#   NETWORK EDITOR SUBMENU
# ======================

NETWORK_EDITOR_MENU = {
    "title": "Edit Network Settings",
    "context": {
        "title": "",
        "fields": [
            ("Target IP", get_target_ip),
            ("FQDNs", get_fqdn_count),
        ]
    },
    "items": {
        "Fields": {
            "1": ("Edit IP Address", wrap_edit_network_field),
            "2": ("Edit Domain", wrap_edit_network_field),
            "3": ("Edit Domain Name", wrap_edit_network_field),
            "4": ("Edit Domain Controller", wrap_edit_network_field),
        },
        "FQDN Management": {
            "5": ("Add FQDN", add_fqdn),
            "6": ("Remove FQDN", remove_fqdn),
            "7": ("List FQDNs", list_fqdns),
        },

    }
}

FQDN_MANAGEMENT_MENU = {
    "title": "FQDN Management",
    "items": {
        "Actions": {
            "1": ("Add FQDN", add_fqdn),
            "2": ("Remove FQDN", remove_fqdn),
            "3": ("List FQDNs", list_fqdns),
        }
    }
}

# ======================
#   CREDENTIALS EDITOR SUBMENU
# ======================

CREDENTIALS_EDITOR_MENU = {
    "title": "Edit Credentials",
    "items": {
        "Fields": {
            "1": ("Edit Username", wrap_edit_credentials_field),
            "2": ("Edit Password", wrap_edit_credentials_field),
        },

    }
}


# ======================
#   CONFIG SUBMENU (Updated)
# ======================

CONFIG_MENU = {
    "title": "Configuration",
    "context": {
        "title": "",
        "fields": [
            ("Lab Name", get_lab_name),
            ("Target IP", get_target_ip),
            ("Platform", get_platform),
        ]
    },
    "items": {
        "Editors": {
            "1": ("Update Target IP", quick_ip_update),
            "2": ("Edit Metadata", METADATA_EDITOR_MENU),
            "3": ("Edit Network Settings", NETWORK_EDITOR_MENU),
            "4": ("Edit Credentials", CREDENTIALS_EDITOR_MENU),
        },
        "View": {
            "5": ("View Full Config", view_config),
        },

    }
}


# ======================
#   HOSTS MANAGEMENT SUBMENU (New)
# ======================

HOSTS_MANAGEMENT_MENU = {
    "title": "/etc/hosts Management",
    "context": {
        "title": "",
        "fields": [
            ("Target IP", get_target_ip),
            ("FQDNs", get_fqdn_count),
        ]
    },
    "items": {
        "Actions": {
            "1": ("Update /etc/hosts", update_hosts),
            "2": ("Remove from /etc/hosts", remove_from_hosts),
            "3": ("View Current Entries", view_hosts_entries),
        },

    }
}


# ======================
#   LAB INFO SUBMENU
# ======================

LAB_INFO_MENU = {
    "title": "Lab Information",
    "items": {
        "View": {
            "1": ("Show Complete Lab Info", wrap_show_lab_info),
            "2": ("View Configuration", view_config),
        },
        "Open Directories": {
            "3": ("Open Notes Directory", wrap_open_notes),
            "4": ("Open Scans Directory", wrap_open_scans),
        },

    }
}


# ======================
#   MAIN MENU
# ======================

MAIN_MENU = {
    "title": get_main_menu_title,  # Dynamic title based on lab name
    "context": None,  # Will be populated dynamically
    "items": {
        "Actions": {
            "1": ("Start/Stop Server", wrap_start_stop_server),
            "2": ("Run Scans", SCANNING_MENU),
            "3": ("Update Target IP", quick_ip_update),
            "4": ("Manage FQDNs", FQDN_MANAGEMENT_MENU),
        },
        "Management": {
            "5": ("Manage Server", SERVER_MANAGEMENT_MENU),  # This will be updated later to SERVER_MANAGEMENT_MENU
            "6": ("Configure Lab", CONFIG_MENU),
            "7": ("Manage /etc/hosts", HOSTS_MANAGEMENT_MENU),
        },
        "Information": {
            "8": ("Quick Commands", wrap_quick_commands),
            "9": ("Lab Info & Files", LAB_INFO_MENU),
        }
    }
}