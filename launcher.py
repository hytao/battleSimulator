#!/usr/bin/env python3
"""
One-click installer and launcher for Battle Simulator
This script will:
1. Check if Python and required packages are installed
2. Install missing packages automatically  
3. Launch the simulator
"""

import subprocess
import sys
import os
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} found")
    return True

def check_and_install_package(package_name, import_name=None):
    """Check if a package is installed, install if missing"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} is already installed")
        return True
    except ImportError:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"✓ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            return False

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print("✓ tkinter is available")
        return True
    except ImportError:
        print("❌ tkinter is not available")
        print("Please install tkinter:")
        print("  Windows: Reinstall Python with tkinter option")
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  CentOS/RHEL: sudo yum install tkinter")
        print("  macOS: brew install python-tk")
        return False

def run_simulator():
    """Launch the battle simulator"""
    print("\n🚀 Starting Battle Simulator...")
    try:
        # Import and run the main function
        import simulator
        simulator.main()
    except KeyboardInterrupt:
        print("\n👋 Simulator closed by user")
    except Exception as e:
        print(f"\n❌ Error running simulator: {e}")
        print("Please check the console output above for details")
        input("Press Enter to continue...")

def main():
    """Main installer and launcher function"""
    print("=" * 50)
    print("🎮 Battle Simulator - One-Click Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check and install required packages
    print("\n📋 Checking dependencies...")
    
    packages_ok = True
    packages_ok &= check_and_install_package("pandas")
    packages_ok &= check_and_install_package("requests")
    packages_ok &= check_tkinter()
    
    if not packages_ok:
        print("\n❌ Some dependencies are missing. Please install them manually.")
        input("Press Enter to exit...")
        return
    
    print("\n✅ All dependencies are ready!")
    
    # Change to script directory to ensure relative imports work
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if simulator.py exists
    if not os.path.exists("simulator.py"):
        print("❌ simulator.py not found in current directory")
        input("Press Enter to exit...")
        return
    
    # Launch the simulator
    run_simulator()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        input("Press Enter to exit...")
