# antivirus_check.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani

import subprocess

def av_win():
    try:
        result = subprocess.check_output([
            "powershell",
            "(Get-MpComputerStatus).AntivirusEnabled"
        ], text=True)
        enabled = "True" in result
        return {
            "status": "Pass" if enabled else "Fail",
            "message": result.strip(),
            "severity": "Low" if enabled else "Medium"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def av_mac():
    print("Checking antivirus status on macOS...")
    gate = subprocess.run(["spctl","--status"], capture_output=True, text=True).stdout
    xpkgs = subprocess.run(["pkgutil","--pkgs"], capture_output=True, text=True).stdout
    enabled = "enabled" in gate
    found   = any("XProtect" in pkg for pkg in xpkgs.splitlines())
    sev = "Low" if (enabled and found) else "Medium"
    return {
        "status":  "Pass" if enabled and found else "Fail",
        "message": ("Gatekeeper on, XProtect found" if enabled and found
                    else "Missing Gatekeeper or XProtect"),
        "severity": sev
    }

def av_linux():
    print("Checking antivirus status on Linux...")
    try:
        import subprocess
        proc = subprocess.run(["pgrep", "clamd"], capture_output=True)
        running = proc.returncode == 0
        return {
            "status":  "Pass" if running else "Fail",
            "message": "clamd running" if running else "clamd not found",
            "severity":"Low" if running else "Medium"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
