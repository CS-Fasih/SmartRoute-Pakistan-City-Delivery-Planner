#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/smartroute"

if [ ! -d "venv" ]; then
    echo -e "\033[0;31m[ERROR] Virtual environment not found.\033[0m"
    echo "        Please run ./setup_linux_macos.sh first."
    exit 1
fi

source venv/bin/activate
python main.py
deactivate 2>/dev/null || true
