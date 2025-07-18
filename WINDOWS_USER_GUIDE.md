# 🎮 Battle Simulator - Windows User Guide (No Python Knowledge Required)

## 🚀 Three Easy Ways to Run the Battle Simulator

### 🎯 Method 1: One-Click Launcher (EASIEST!)

**This is the simplest way - perfect if you're not familiar with programming:**

1. **Download Python** (one-time setup):
   - Go to [python.org](https://python.org)
   - Click "Download Python" (get the latest version)
   - **IMPORTANT**: During installation, check the box "Add Python to PATH"
   - Complete the installation

2. **Run the simulator**:
   - Find the file called `run_simulator.bat` 
   - **Double-click it** - that's it!
   - The first time it runs, it will automatically install everything needed
   - The battle simulator will start automatically

3. **What happens automatically**:
   - ✅ Checks if Python is installed correctly
   - ✅ Downloads and installs required components (pandas, requests)
   - ✅ Starts the battle simulator
   - ✅ Shows helpful error messages if anything goes wrong

---

### 🎯 Method 2: Standalone Executable (BEST FOR SHARING)

**If you want to create a version that works on any Windows computer without Python:**

1. **First, use Method 1 above to get Python installed**

2. **Create the standalone version**:
   - Double-click `run_simulator.bat` once to make sure everything works
   - Open Command Prompt (search "cmd" in Start menu)
   - Navigate to the simulator folder:
     ```
     cd "C:\path\to\your\simulator\folder"
     ```
   - Run this command:
     ```
     python build_exe.py
     ```

3. **Use the standalone version**:
   - You'll find a new file: `dist/BattleSimulator.exe`
   - This .exe file can run on ANY Windows computer
   - No Python installation needed on other computers!
   - Just copy and share the .exe file

---

### 🎯 Method 3: Manual Installation (FOR TECH-SAVVY USERS)

If you're comfortable with command lines:

1. Install Python from [python.org](https://python.org)
2. Open Command Prompt and run:
   ```
   pip install pandas requests
   cd "path\to\simulator\folder"
   python simulator.py
   ```

---

## 📋 Quick Troubleshooting

### ❌ "Python is not recognized"
- **Solution**: Reinstall Python and check "Add Python to PATH" during installation
- **Alternative**: Use Method 2 to create the standalone .exe file

### ❌ "Permission denied" or installation errors
- **Solution**: Run Command Prompt as Administrator
- **Alternative**: The smart launcher uses `--user` installation to avoid this

### ❌ Google Sheets not loading
- **Solution**: Check the [Google Sheets Guide](GOOGLE_SHEETS_GUIDE.md) for proper URL format and sharing settings

### ❌ Battle simulator crashes or won't start
- **Solution**: Try running `run_simulator.bat` again - it includes error reporting

---

## 🎮 How to Use the Battle Simulator

1. **Starting**: Double-click `run_simulator.bat` or the .exe file
2. **Google Sheets URL**: The program will ask for your Google Sheets URL
   - Copy your Google Sheets sharing URL
   - Paste it into the dialog box
   - The URL gets saved for next time!
3. **Battle Controls**:
   - **Continue**: Advance to next battle step
   - **Auto-play**: Let battles run automatically
   - **Debug Mode**: See detailed damage calculations
   - **End Battle**: Stop the current battle

---

## 📁 Important Files

- `run_simulator.bat` - **Double-click this to start!**
- `simulator.py` - Main program (don't need to touch)
- `launcher.py` - Smart installer (don't need to touch)
- `build_exe.py` - Creates standalone .exe version
- `requirements.txt` - List of needed components
- `README.md` - Technical documentation
- `GOOGLE_SHEETS_GUIDE.md` - How to set up your Google Sheets

---

## 💡 Tips for Non-Programmers

1. **Keep it simple**: Just use `run_simulator.bat` - it handles everything
2. **One-time setup**: You only need to install Python once
3. **Save your URLs**: The program remembers your Google Sheets URL
4. **Share easily**: Create the .exe version to share with others
5. **Get help**: All error messages include helpful suggestions

---

## 🆘 Need More Help?

- **Google Sheets setup**: See `GOOGLE_SHEETS_GUIDE.md`
- **Distribution options**: See `DISTRIBUTION_GUIDE.md`
- **Technical details**: See `README.md`

**Remember**: The `run_simulator.bat` file does almost everything automatically - just double-click it!
