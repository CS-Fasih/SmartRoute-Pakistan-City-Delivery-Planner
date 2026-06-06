#!/usr/bin/env bash
set -e

# ================================================================
#  SmartRoute — Pakistan City Delivery Planner
#  Setup Script for Linux & macOS
# ================================================================

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

echo -e "${CYAN}================================================================${RESET}"
echo -e "${CYAN}         SmartRoute — Pakistan City Delivery Planner${RESET}"
echo -e "${CYAN}         Setup Script for Linux & macOS${RESET}"
echo -e "${CYAN}================================================================${RESET}"
echo ""

# Step 1: Check Python installation
echo -e "${YELLOW}[1/5] Checking Python installation...${RESET}"

if command -v python3 &>/dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &>/dev/null; then
    PYTHON=python
    PIP=pip
else
    echo -e "${RED}[ERROR] Python is not installed.${RESET}"
    echo "        Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON --version 2>&1)
echo "        Found $PYTHON_VERSION"
echo ""

# Step 2: Install system dependencies (Linux only)
echo -e "${YELLOW}[2/5] Checking system dependencies...${RESET}"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Check for tkinter
    if $PYTHON -c "import tkinter" &>/dev/null; then
        echo "        tkinter is available."
    else
        echo "        tkinter not found. Attempting to install..."
        if command -v apt-get &>/dev/null; then
            echo "        Running: sudo apt-get install -y python3-tk"
            sudo apt-get update -qq
            sudo apt-get install -y python3-tk
        elif command -v dnf &>/dev/null; then
            echo "        Running: sudo dnf install -y python3-tkinter"
            sudo dnf install -y python3-tkinter
        elif command -v pacman &>/dev/null; then
            echo "        Running: sudo pacman -S --noconfirm tk"
            sudo pacman -S --noconfirm tk
        elif command -v zypper &>/dev/null; then
            echo "        Running: sudo zypper install -y python3-tk"
            sudo zypper install -y python3-tk
        else
            echo -e "${RED}[WARNING] Could not detect package manager.${RESET}"
            echo "         Please install tkinter manually (python3-tk or tk package)."
        fi
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "        macOS detected. tkinter is bundled with Python from python.org."
    echo "        If using Homebrew Python, run: brew install python-tk"
fi
echo ""

# Step 3: Navigate to project directory
echo -e "${YELLOW}[3/5] Navigating to project directory...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/smartroute"
echo "        Working in: $PWD"
echo ""

# Step 4: Create virtual environment
echo -e "${YELLOW}[4/5] Setting up virtual environment...${RESET}"
if [ -d "venv" ]; then
    echo "        Virtual environment already exists. Skipping creation."
else
    $PYTHON -m venv venv
    echo -e "        ${GREEN}Virtual environment created.${RESET}"
fi
echo ""

# Step 5: Activate and install dependencies
echo -e "${YELLOW}[5/5] Installing dependencies...${RESET}"
source venv/bin/activate
$PIP install --upgrade pip --quiet
$PIP install -r requirements.txt
echo ""

echo -e "${CYAN}================================================================${RESET}"
echo -e "${GREEN}  Setup Complete!${RESET}"
echo -e "${CYAN}================================================================${RESET}"
echo ""
echo "  To run SmartRoute:"
echo "    cd smartroute"
echo "    source venv/bin/activate"
echo "    python main.py"
echo ""
echo "  Or simply run:"
echo "    ./run.sh"
echo ""

read -p "  Press Enter to launch SmartRoute now..." -r
python main.py
deactivate 2>/dev/null || true
