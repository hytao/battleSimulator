#!/usr/bin/env python3
"""
Build script to create an executable from the battle simulator.
Run this script to create a standalone .exe file that can be run without Python installed.
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_executable():
    """Create executable using PyInstaller"""
    print("Creating executable...")
    
    # PyInstaller command with options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # No console window (GUI only)
        "--name", "BattleSimulator",  # Name of the executable
        "--icon", "icon.ico",  # Add icon if available (optional)
        "--add-data", "*.py;.",  # Include all Python files
        "--hidden-import", "tkinter",  # Ensure tkinter is included
        "--hidden-import", "pandas",  # Ensure pandas is included
        "--hidden-import", "requests",  # For Google Sheets access
        "simulator.py"  # Main script
    ]
    
    # Remove icon option if no icon file exists
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon")
        cmd.remove("icon.ico")
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Executable created successfully!")
        print("📁 Check the 'dist' folder for 'BattleSimulator.exe'")
        print("🚀 You can now distribute this .exe file to run the simulator without Python!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating executable: {e}")
        return False
    
    return True

def cleanup_build_files():
    """Clean up temporary build files"""
    import shutil
    
    for folder in ["build", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Cleaned up {folder}/")
    
    if os.path.exists("BattleSimulator.spec"):
        os.remove("BattleSimulator.spec")
        print("🧹 Cleaned up BattleSimulator.spec")

if __name__ == "__main__":
    print("=== Battle Simulator Executable Builder ===\n")
    
    # Check if we're in the right directory
    if not os.path.exists("simulator.py"):
        print("❌ simulator.py not found. Please run this script in the same directory as simulator.py")
        sys.exit(1)
    
    try:
        install_pyinstaller()
        success = create_executable()
        
        if success:
            print("\n=== Build Complete ===")
            print("📋 What you get:")
            print("  • dist/BattleSimulator.exe - Standalone executable")
            print("  • No Python installation required on target machines")
            print("  • All dependencies included")
            
            cleanup_choice = input("\n🧹 Clean up temporary build files? (y/N): ")
            if cleanup_choice.lower() == 'y':
                cleanup_build_files()
            
            print("\n🎮 Ready to share your Battle Simulator!")
        
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
