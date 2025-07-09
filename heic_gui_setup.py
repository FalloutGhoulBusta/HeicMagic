#!/usr/bin/env python3
"""
Setup script for HEIC Converter GUI
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    packages = [
        "pillow-heif>=0.10.0",
        "Pillow>=9.0.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    return True

def create_desktop_shortcut():
    """Create desktop shortcut (Windows and Linux)"""
    try:
        import platform
        system = platform.system()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gui_script = os.path.join(script_dir, "heic_converter_gui.py")
        
        if system == "Windows":
            # Create Windows shortcut
            try:
                import win32com.client
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                shortcut_path = os.path.join(desktop, "HEIC Converter.lnk")
                
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = f'"{gui_script}"'
                shortcut.WorkingDirectory = script_dir
                shortcut.save()
                
                print(f"✓ Desktop shortcut created: {shortcut_path}")
            except ImportError:
                print("⚠ pywin32 not installed, skipping shortcut creation")
                print("  Install with: pip install pywin32")
        
        elif system == "Linux":
            # Create Linux desktop entry
            desktop_file_content = f"""[Desktop Entry]
Name=HEIC Converter
Comment=Convert HEIC images to JPEG/PNG
Exec={sys.executable} "{gui_script}"
Icon=image-x-generic
Terminal=false
Type=Application
Categories=Graphics;Photography;
"""
            
            desktop_dir = os.path.expanduser("~/Desktop")
            if os.path.exists(desktop_dir):
                desktop_file_path = os.path.join(desktop_dir, "heic-converter.desktop")
                with open(desktop_file_path, "w") as f:
                    f.write(desktop_file_content)
                
                # Make executable
                os.chmod(desktop_file_path, 0o755)
                print(f"✓ Desktop shortcut created: {desktop_file_path}")
            else:
                print("⚠ Desktop directory not found, skipping shortcut creation")
        
        else:
            print("⚠ Shortcut creation not supported on this platform")
    
    except Exception as e:
        print(f"⚠ Could not create desktop shortcut: {e}")

def main():
    print("HEIC Converter GUI Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        print("✗ Failed to install requirements")
        sys.exit(1)
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\nSetup completed!")
    print("\nTo run the application:")
    print("  python heic_converter_gui.py")
    print("\nOr use the desktop shortcut if created.")

if __name__ == "__main__":
    main()