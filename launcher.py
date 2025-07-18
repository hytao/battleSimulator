#!/usr/bin/env python3
"""
Smart launcher for Battle Simulator
This script will:
1. Check Python version compatibility
2. Check if required packages are installed
3. Install missing packages automatically  
4. Launch the simulator with proper error handling
5. Provide helpful troubleshooting information
"""

import subprocess
import sys
import os
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python from: https://python.org")
        return False
    print(f"✓ Python {sys.version.split()[0]} found (compatible)")
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
            # Use --user flag for user installation to avoid permission issues
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--user", package_name
            ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"✓ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            print(f"   Try manually: pip install {package_name}")
            return False

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print("✓ tkinter is available")
        return True
    except ImportError:
        print("❌ tkinter is not available")
        print("   Platform-specific installation:")
        print("   Windows: Reinstall Python with tkinter option checked")
        print("   Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   CentOS/RHEL: sudo yum install tkinter")
        print("   macOS: brew install python-tk")
        return False

def check_simulator_file():
    """Check if simulator.py exists and is readable"""
    if not os.path.exists("simulator.py"):
        print("❌ simulator.py not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        print("   Please run this script from the Battle Simulator directory")
        return False
    
    # Check if file is readable
    try:
        with open("simulator.py", 'r', encoding='utf-8') as f:
            content = f.read(100)  # Read first 100 chars to test
        print("✓ simulator.py found and readable")
        return True
    except Exception as e:
        print(f"❌ Cannot read simulator.py: {e}")
        return False

def run_simulator():
    """Launch the battle simulator with error handling"""
    print("\n🚀 Starting Battle Simulator...")
    print("-" * 40)
    
    try:
        # Change to script directory to ensure relative imports work
        script_dir = os.path.dirname(os.path.abspath(__file__))
        original_dir = os.getcwd()
        os.chdir(script_dir)
        
        try:
            # Import and run the main function
            import simulator
            if hasattr(simulator, 'main'):
                simulator.main()
            else:
                print("❌ No main() function found in simulator.py")
                print("   This might be an older version of the simulator")
                print("   Try running: python simulator.py")
        finally:
            # Restore original directory
            os.chdir(original_dir)
            
    except KeyboardInterrupt:
        print("\n👋 Simulator closed by user (Ctrl+C)")
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("   This usually means missing dependencies")
        print("   Try running the launcher again to reinstall packages")
    except Exception as e:
        print(f"\n❌ Unexpected error running simulator: {e}")
        print("   Please check the error message above")
        print("   You can also try: python simulator.py")
        
        # Offer to run tests
        try:
            choice = input("\n🧪 Would you like to run the test suite? (y/N): ").lower()
            if choice == 'y':
                # import test_comprehensive
                # test_comprehensive.run_all_tests()
                print("   Test suite not available in this version")
        except:
            pass
        
        input("\nPress Enter to continue...")

def print_system_info():
    """Print helpful system information"""
    print(f"💻 System Information:")
    print(f"   OS: {os.name}")
    print(f"   Python executable: {sys.executable}")
    print(f"   Python path: {sys.path[0]}")
    print(f"   Working directory: {os.getcwd()}")

def main():
    """Main installer and launcher function"""
    print("=" * 60)
    print("🎮 Battle Simulator - Smart Launcher")
    print("=" * 60)
    
    # Print system info for debugging
    print_system_info()
    print()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check if simulator file exists
    if not check_simulator_file():
        input("Press Enter to exit...")
        return
    
    # Check and install required packages
    print("\n📋 Checking dependencies...")
    
    packages_ok = True
    packages_ok &= check_and_install_package("pandas")
    packages_ok &= check_and_install_package("requests")
    packages_ok &= check_tkinter()
    
    if not packages_ok:
        print("\n❌ Some dependencies are missing.")
        print("   You can try to install them manually:")
        print("   pip install pandas requests")
        print("   (tkinter usually comes with Python)")
        
        choice = input("\n🚀 Try to run simulator anyway? (y/N): ").lower()
        if choice != 'y':
            input("Press Enter to exit...")
            return
    else:
        print("\n✅ All dependencies are ready!")
    
    # Launch the simulator
    run_simulator()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Launcher cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        input("Press Enter to exit...")
