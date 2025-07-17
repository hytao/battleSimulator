# Battle Simulator Setup and Installation Guide

## Features
- **Google Sheets Integration**: Load battle data directly from your Google Sheets
- **Large URL Input GUI**: User-friendly interface for entering Google Sheets URLs
- **Auto-Play Mode**: Automatic battle progression with 2-second intervals
- **Interactive GUI**: User-friendly interface for battle simulation
- **Automatic URL Parsing**: Supports various Google Sheets URL formats
- **Debug Mode**: Toggle detailed logging for troubleshooting
- **Real-time Battle Visualization**: Visual map with unit positions and status

## Easy Installation Options

### Option 1: Double-Click Launcher (Recommended for Windows)
1. Make sure Python is installed on your system
2. Double-click `run_simulator.bat` to start the simulator
3. The launcher will automatically check dependencies and run the simulator

### Option 2: Create Standalone Executable (Best for Distribution)
1. Run the build script: `python build_exe.py`
2. This creates `dist/BattleSimulator.exe` - a standalone executable
3. Share the .exe file - no Python installation needed on target machines!

### Option 3: Manual Python Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the simulator
python simulator.py
```

## How to Use

### Setting Up Your Google Sheets Data
1. When you run the simulator, you'll be prompted to enter your Google Sheets URL
2. **Supported URL formats:**
   - `https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=GID`
   - `https://docs.google.com/spreadsheets/d/SHEET_ID/edit?gid=GID`
   - `https://docs.google.com/spreadsheets/d/SHEET_ID/edit?usp=sharing&gid=GID#gid=GID`

3. **Make sure your Google Sheet is publicly accessible:**
   - Click "Share" in your Google Sheets
   - Change permissions to "Anyone with the link can view"
   - Copy the sharing URL and paste it into the simulator

### Example Google Sheets URL
```
https://docs.google.com/spreadsheets/d/1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo/edit?gid=489835885#gid=489835885
```

### Running the Simulation
1. Start the simulator using any of the installation options above
2. **New Large URL Input GUI**: A user-friendly dialog will appear with:
   - Clear instructions and examples
   - Large input field for your Google Sheets URL
   - Setup guide for making your sheet accessible
   - Options to proceed, cancel, or use test mode
3. Enter your Google Sheets URL when prompted
4. The simulator will parse the URL and load your battle data
5. If loading fails, you can choose to use test mode instead
6. **Battle Interface Features**:
   - **Debug Toggle**: Click "開啟DEBUG" to see detailed combat information
   - **Auto-Play Mode**: Click "自動播放" to automatically continue battle every 2 seconds
   - **Manual Control**: Use Continue button or press any key to proceed manually
   - **End Battle**: Stop the simulation at any time
7. Follow the on-screen instructions to run the battle simulation

## System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Internet connection (for Google Sheets data)

## Dependencies
- `pandas` - Data manipulation
- `requests` - HTTP requests for Google Sheets
- `tkinter` - GUI framework (usually included with Python)

## Troubleshooting

### "Python is not recognized"
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation

### "tkinter not found"
- **Windows**: Reinstall Python with tkinter option checked
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter`
- **macOS**: `brew install python-tk`

### "Module not found" errors
Run: `pip install pandas requests`

## File Structure
```
battleSimulator/
├── simulator.py          # Main simulator code
├── run_simulator.bat     # Windows launcher
├── run_simulator.sh      # Linux/Mac launcher  
├── build_exe.py         # Executable builder
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── test_*.py           # Test scripts
```

## Creating a Desktop Shortcut (Windows)
1. Right-click on `run_simulator.bat`
2. Select "Create shortcut"
3. Move the shortcut to your desktop
4. Rename it to "Battle Simulator"
5. Right-click shortcut → Properties → Change Icon (optional)

## Distribution Options

### For Technical Users
Share the entire folder with the launcher scripts

### For Non-Technical Users  
1. Run `python build_exe.py` to create standalone executable
2. Share only the `dist/BattleSimulator.exe` file
3. No Python installation required on target machines

## Advanced Usage
- All test scripts can be run directly: `python test_*.py`
- Debug mode available in the GUI
- Google Sheets data is automatically fetched and cached
simulator
