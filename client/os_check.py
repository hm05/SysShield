# os_check.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani

import subprocess

def os_win():
    print("Checking Windows update status...")
    try:
        return {
            "status": "Info",
            "message": "Update status check not yet implemented for Windows.",
            "severity": "Low"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def os_linux():
    print("Checking Linux update status...")
    try:
        # Refresh metadata quietly
        subprocess.run(
            ["apt-get", "update"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Simulate upgrade to see what would change
        proc = subprocess.run(
            ["apt-get", "-s", "upgrade"],
            capture_output=True, text=True, check=True
        )

        # “Inst ” lines show packages that would install/upgrade
        lines = [l for l in proc.stdout.splitlines() if l.startswith("Inst ")]
        total = len(lines)
        kernel = sum(1 for l in lines if "linux-image" in l or "linux-headers" in l)
        severity = "High" if kernel else ("Medium" if total else "Low")

        return {
            "status": "Pass" if total == 0 else "Fail",
            "total": total,
            "kernel": kernel,
            "details": lines,
            "severity": severity
        }

    except subprocess.CalledProcessError as e:
        return {"status": "Error", "message": f"apt error: {e}"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


def os_mac():
    print("Checking macOS update status...")
    try:
        result = subprocess.run(["softwareupdate", "-l"], capture_output=True, text=True)
        lines = [l for l in result.stdout.splitlines() if l.strip().startswith("*")]

        if not lines:
            return {"status": "Pass", "details": [], "severity": "Low"}

        os_upd = [l for l in lines if "macOS" in l or "Sequoia" in l]
        severity = "Medium" if os_upd else "Low"

        return {"status": "Fail", "details": lines, "severity": severity}

    except Exception as e:
        return {"status": "Error", "message": str(e)}