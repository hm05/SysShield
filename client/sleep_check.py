# sleep_check.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani
import subprocess

def sleep_win():
    print("Checking sleep settings on Windows...")
    return {"status":"Info","message":"Sleep check not implemented for Windows.","severity":"Low"}

def sleep_mac():
    print("Checking sleep settings on macOS...")
    out = subprocess.run(["pmset","-g"], capture_output=True, text=True).stdout
    modes = {}
    for line in out.splitlines():
        if "standbydelay" in line or "hibernatemode" in line:
            key,val = line.split()[0], line.split()[1]
            modes[key] = val
    ok = int(modes.get("hibernatemode",1)) in (0,3)
    return {
        "status":  "Pass" if ok else "Fail",
        "message": f"Sleep modes: {modes}",
        "severity":"Low"
    }

def sleep_linux():
    print("Checking sleep settings on Linux...")
    try:
        with open("/sys/power/state") as f:
            states = f.read().split()
        return {
            "status": "Pass" if "mem" in states else "Fail",
            "message": f"Supported states: {', '.join(states)}",
            "severity": "Low"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
