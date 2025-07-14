# sleep_check.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani
import platform
import subprocess

def sleep_win():
    print("Checking sleep settings on Windows...")
    try:
        result = subprocess.run(["powercfg", "-query"], capture_output=True, text=True)
        return "Sleep timeout check not yet implemented"
    except Exception as e:
        return f"Error: {e}"

def sleep_linux():
    print("Checking sleep settings on Linux...")
    try:
        result = subprocess.run(["gsettings", "get", "org.gnome.settings-daemon.plugins.power", "sleep-inactive-ac-timeout"], capture_output=True, text=True)
        return int(result.stdout.strip()) <= 600  # 10 mins
    except Exception as e:
        return f"Error: {e}"

def sleep_mac():
    print("Checking sleep settings on macOS...")
    try:
        result = subprocess.run(["pmset", "-g", "custom"], capture_output=True, text=True)
        return "Sleep settings check not yet implemented"
    except Exception as e:
        return f"Error: {e}"
