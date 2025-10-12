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

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     labcmdr - Installation               ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}\n"

# Check if labcmdr.py exists
if [ ! -f "$LABCMDR_SCRIPT" ]; then
    echo -e "${RED}[!] Error: labcmdr.py not found in ${SCRIPT_DIR}${NC}"
    exit 1
fi

# Make executable
echo -e "${YELLOW}[*] Making labcmdr.py executable...${NC}"
chmod +x "$LABCMDR_SCRIPT"
echo -e "${GREEN}[+] Done${NC}\n"

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
    
    echo -e "${BLUE}Usage:${NC}"
    echo -e "  labcmdr create          # Create new lab"
    echo -e "  labcmdr start           # Start lab"
    echo -e "  labcmdr status          # Show status"
    echo -e "  labcmdr --help          # Show help\n"
    
    echo -e "${BLUE}Test it:${NC}"
    echo -e "  labcmdr --help\n"
else
    echo -e "${RED}[!] Installation failed - symlink not executable${NC}"
    exit 1
fi

echo -e "${GREEN}Ready to hack! 🚀${NC}"