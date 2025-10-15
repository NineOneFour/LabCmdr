#!/usr/bin/env bash
# install.sh - Install labcmdr tool

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LABCMDR_SCRIPT="${SCRIPT_DIR}/labcmdr.py"
DEFAULT_CONFIG="${SCRIPT_DIR}/src/templates/default_config.yaml"
CONFIG_DIR="${HOME}/.config/labcmdr"
CONFIG_FILE="${CONFIG_DIR}/config.yaml"

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     labcmdr - Installation               ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}\n"

# Check for envsubst
if ! command -v envsubst &> /dev/null; then
    echo -e "${RED}[!] Error: envsubst not found${NC}"
    echo -e "${YELLOW}[*] Install it with: sudo apt install gettext${NC}"
    echo -e "${YELLOW}[*] Or on other distros: yum/dnf/pacman install gettext${NC}"
    exit 1
fi

# Check if labcmdr.py exists
if [ ! -f "$LABCMDR_SCRIPT" ]; then
    echo -e "${RED}[!] Error: labcmdr.py not found in ${SCRIPT_DIR}${NC}"
    exit 1
fi

# Check if default_config.yaml exists
if [ ! -f "$DEFAULT_CONFIG" ]; then
    echo -e "${RED}[!] Error: default_config.yaml not found in ${SCRIPT_DIR}/src/templates/${NC}"
    exit 1
fi

# Make executable
echo -e "${YELLOW}[*] Making labcmdr.py executable...${NC}"
chmod +x "$LABCMDR_SCRIPT"
echo -e "${GREEN}[+] Done${NC}\n"

# Setup config directory and file
echo -e "${YELLOW}[*] Setting up configuration...${NC}"

# Create config directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo -e "${YELLOW}[*] Creating ${CONFIG_DIR}...${NC}"
    mkdir -p "$CONFIG_DIR"
    echo -e "${GREEN}[+] Created${NC}"
fi

# Copy config file if it doesn't exist
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${GREEN}[+] Config file already exists: ${CONFIG_FILE}${NC}"
    echo -e "${YELLOW}[*] Keeping existing configuration${NC}"
else
    echo -e "${YELLOW}[*] Creating config file...${NC}"
    
    # Copy and substitute $HOME in the config file
    # This expands $HOME to the actual home directory path
    envsubst < "$DEFAULT_CONFIG" > "$CONFIG_FILE"
    
    echo -e "${GREEN}[+] Config file created: ${CONFIG_FILE}${NC}"
fi

echo -e "${GREEN}[+] Configuration complete${NC}\n"

# Install to user directory
INSTALL_DIR="${HOME}/.local/bin"
echo -e "${YELLOW}[*] Installing to ${INSTALL_DIR}${NC}"

# Create .local/bin if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}[*] Creating ${INSTALL_DIR}...${NC}"
    mkdir -p "$INSTALL_DIR"
    echo -e "${GREEN}[+] Created${NC}"
fi

# Check if .local/bin is in PATH
if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
    echo -e "${YELLOW}[!] Warning: ${INSTALL_DIR} is not in your PATH${NC}"
    echo -e "${YELLOW}[*] Add this to your ~/.bashrc or ~/.zshrc:${NC}"
    echo -e "${BLUE}    export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}\n"
fi

# Create or update symlink
SYMLINK_PATH="${INSTALL_DIR}/labcmdr"

if [ -L "$SYMLINK_PATH" ]; then
    echo -e "${YELLOW}[*] Removing existing symlink...${NC}"
    rm "$SYMLINK_PATH"
fi

echo -e "${YELLOW}[*] Creating symlink...${NC}"
ln -s "$LABCMDR_SCRIPT" "$SYMLINK_PATH"
echo -e "${GREEN}[+] Symlink created: ${SYMLINK_PATH} -> ${LABCMDR_SCRIPT}${NC}\n"

# Verify installation
if [ -x "$SYMLINK_PATH" ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     Installation Successful!             ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}\n"
    
    echo -e "${BLUE}Configuration:${NC}"
    echo -e "  Config file: ${CONFIG_FILE}"
    echo -e "  Edit with:   labcmdr config edit"
    echo -e "  View with:   labcmdr config show\n"
    
    echo -e "${BLUE}Usage:${NC}"
    echo -e "  labcmdr create          # Create new lab"
    echo -e "  labcmdr run             # Start lab control panel"
    echo -e "  labcmdr status          # Show status"
    echo -e "  labcmdr config          # Manage configuration"
    echo -e "  labcmdr --help          # Show help\n"
    
    echo -e "${BLUE}Test it:${NC}"
    echo -e "  labcmdr --help\n"
else
    echo -e "${RED}[!] Installation failed - symlink not executable${NC}"
    exit 1
fi

echo -e "${GREEN}Get to Hacking! ${NC}"