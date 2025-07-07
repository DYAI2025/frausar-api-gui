#!/usr/bin/env python3
"""
Build script for Tax Calculator Storage
Creates standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_tax_calculator():
    """Build standalone executable"""
    
    print("Building Tax Calculator Storage...")
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if tax_calculator.py exists
    if not Path("tax_calculator.py").exists():
        print("Error: tax_calculator.py not found!")
        return False
    
    # PyInstaller command
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "TaxCalculatorStorage",
        "--hidden-import", "cryptography",
        "--clean",
        "tax_calculator.py"
    ]
    
    try:
        # Run PyInstaller
        print("Running PyInstaller...")
        subprocess.run(pyinstaller_cmd, check=True)
        
        print("Build successful!")
        
        # Move executable to main directory
        if sys.platform == "win32":
            exe_path = Path("dist/TaxCalculatorStorage.exe")
            final_path = Path("TaxCalculatorStorage.exe")
        elif sys.platform == "darwin":
            exe_path = Path("dist/TaxCalculatorStorage.app")
            final_path = Path("TaxCalculatorStorage.app")
        else:
            exe_path = Path("dist/TaxCalculatorStorage")
            final_path = Path("TaxCalculatorStorage")
            
        if exe_path.exists():
            if final_path.exists():
                if final_path.is_dir():
                    shutil.rmtree(final_path)
                else:
                    final_path.unlink()
                    
            shutil.move(str(exe_path), str(final_path))
            print(f"Executable created: {final_path}")
            
            # Clean up
            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("dist", ignore_errors=True)
            if os.path.exists("TaxCalculatorStorage.spec"):
                os.remove("TaxCalculatorStorage.spec")
                
            print("Build files cleaned up")
            
            return True
        else:
            print("Error: Executable not found!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # Check dependencies
    print("Checking dependencies...")
    
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    try:
        import cryptography
    except ImportError:
        print("Installing cryptography...")
        subprocess.run([sys.executable, "-m", "pip", "install", "cryptography"], check=True)
    
    # Build the application
    success = build_tax_calculator()
    
    if success:
        print("\nTax Calculator Storage is ready!")
        print("Double-click the executable to run.")
    else:
        print("\nBuild failed. Please check error messages.")
        sys.exit(1) 