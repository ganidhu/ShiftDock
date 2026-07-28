#!/bin/bash
set -e

GREEN='\033[32m'
CYAN='\033[36m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'
BOLD='\033[1m'

echo -e "${BOLD}${GREEN}┌────────────────────────────────────────────────────────┐${RESET}"
echo -e "${BOLD}${GREEN}│                 ShiftDock Installer                    │${RESET}"
echo -e "${BOLD}${GREEN}└────────────────────────────────────────────────────────┘${RESET}"
echo

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python3 &> /dev/null; then
    echo -e "  ${RED}Error: Python 3 is required but could not be found.${RESET}"
    exit 1
fi

if command -v pipx &> /dev/null; then
    echo -e "  ${CYAN}Installing via pipx (recommended isolated environment)…${RESET}"
    pipx install "$SCRIPT_DIR" --force
elif command -v pip3 &> /dev/null; then
    echo -e "  ${CYAN}Installing via pip3 (editable)…${RESET}"
    pip3 install -e "$SCRIPT_DIR" --break-system-packages
elif command -v pip &> /dev/null; then
    echo -e "  ${CYAN}Installing via pip (editable)…${RESET}"
    pip install -e "$SCRIPT_DIR" --break-system-packages
else
    echo -e "  ${RED}Error: Neither pipx nor pip could be found.${RESET}"
    exit 1
fi

echo
if command -v shiftdock &> /dev/null; then
    echo -e "  ${BOLD}${GREEN}✓ Installation complete!${RESET}"
    echo -e "  Run from any directory:"
    echo -e "  ${BOLD}${YELLOW}shiftdock${RESET}"
else
    echo -e "  ${YELLOW}Installed, but command not on PATH yet.${RESET}"
    echo -e "  Try: ${BOLD}python3 -m shiftdock_cli.cli${RESET}"
    echo -e "  Or ensure pipx/pip scripts dir is on your PATH."
fi
echo
