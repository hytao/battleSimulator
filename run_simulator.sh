#!/bin/bash
# Battle Simulator - Easy Launcher for Linux/Mac
echo "=== Battle Simulator - Easy Launcher ==="
echo ""
echo "Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from your package manager"
    exit 1
fi

echo "Python found! Starting Battle Simulator..."
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Run the simulator
python3 simulator.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to run simulator"
    echo "Make sure all required packages are installed:"
    echo "  pip3 install pandas requests tkinter"
    read -p "Press Enter to continue..."
fi
