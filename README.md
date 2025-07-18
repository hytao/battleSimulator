# Battle Simulator - Advanced Tactical RPG Combat System

## 🎮 Features
- **📊 Google Sheets Integration**: Load battle data directly from your Google Sheets
- **🖥️ Large URL Input GUI**: User-friendly interface for entering Google Sheets URLs with URL caching
- **⚡ Auto-Play Mode**: Automatic battle progression with 2-second intervals
- **🎯 Interactive GUI**: Beautiful battle visualization with real-time map updates
- **🔗 Automatic URL Parsing**: Supports various Google Sheets URL formats
- **🐛 Debug Mode**: Toggle detailed logging for damage calculation and combat mechanics
- **📍 Real-time Battle Visualization**: Visual map with unit positions, status effects, and movement paths
- **💀 Advanced Combat System**: Support for overkill damage, status effects, and dead unit tracking
- **🛡️ Status Effects**: Support for attack reduction (減攻), defense reduction (減防), and vulnerability (易傷)
- **🎯 Smart Targeting**: Intelligent movement and targeting system
- **🔄 Movement System**: Pathfinding and range calculation with visual feedback

## 🚀 Easy Installation Options

### Option 1: One-Click Launcher (Recommended)
1. **Windows**: Double-click `run_simulator.bat`
2. **Linux/Mac**: Run `./run_simulator.sh` or `bash run_simulator.sh`
3. The smart launcher will automatically:
   - Check Python installation
   - Install missing dependencies
   - Launch the simulator

### Option 2: Create Standalone Executable (Best for Distribution)
1. Run the build script: `python build_exe.py`
2. This creates `dist/BattleSimulator.exe` - a standalone executable
3. Share the .exe file - no Python installation needed on target machines!
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

### Running the Battle Simulation
1. Start the simulator using any installation option above
2. **Enhanced URL Input GUI** will appear with:
   - 📝 Clear instructions and examples
   - 📏 Large, scrollable input field for long Google Sheets URLs
   - 📚 Step-by-step setup guide for making your sheet accessible
   - 💾 Automatic URL caching (remembers your last URL)
   - 🗑️ Clear cache option
   - ✅ Options to proceed, cancel, or use test mode
3. Enter your Google Sheets URL when prompted
4. The simulator will parse the URL and load your battle data
5. If loading fails, you can choose to use test mode instead
6. **Enhanced Battle Interface Features**:
   - **🐛 Debug Toggle**: Click "開啟DEBUG"/"關閉DEBUG" to see detailed combat calculations
   - **⚡ Auto-Play Mode**: Click "自動播放"/"停止自動" for automatic progression (2-second intervals)
   - **🎮 Manual Control**: Use Continue button or press any key to proceed step-by-step
   - **🛑 End Battle**: Stop the simulation at any time
   - **📊 Real-time Map**: Visual representation with unit positions, HP, status effects
   - **📍 Movement Paths**: See unit movement with highlighted paths
   - **💀 Dead Unit Display**: Shows "被擊毀" with overkill damage for eliminated units
7. Follow the on-screen battle progression and enjoy the tactical combat!

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
