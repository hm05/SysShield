# __init__.py
# 🛡️ SysShield System Utility
# Developed by Harsh Murjani

__version__ = "1.0.0"
__author__ = "Harsh Murjani"

import os, sys, subprocess, platform
import json
import atexit
import time
from datetime import datetime
from pathlib import Path

from disk_check import disk_win, disk_linux, disk_mac
from os_check   import os_win,    os_linux,    os_mac
from sleep_check   import sleep_win,   sleep_linux,   sleep_mac
from antivirus_check import av_win,    av_linux,    av_mac

CACHE_PATH = "os_cache.json"
LOG_PATH   = "sysshield_logs.json"

def run_sysshield_loop(interval=1800):  # every 30 minutes
    pid_file = Path("sysshield.pid")
    pid_file.write_text(str(os.getpid()))
    while True:
        run_sysshield()
        time.sleep(interval)

def detect_os():
    return {
        "Windows": "windows",
        "Linux":   "linux",
        "Darwin":  "macos"
    }.get(platform.system(), "unknown")

def load_cached_os():
    try:
        with open(CACHE_PATH) as f:
            return json.load(f)["os"]
    except Exception:
        os_name = detect_os()
        with open(CACHE_PATH, "w") as f:
            json.dump({"os": os_name}, f)
        return os_name

def boot_banner():
    print("\n🛡️  SysShield Client - v1.0.0")
    print(f"⏱️  Start Time: {datetime.now():%Y-%m-%d %H:%M:%S}\n")

def log_results(timestamp, os_type, results):
    entry = {"timestamp": timestamp, "os": os_type, "results": results}
    try:
        with open(LOG_PATH) as f:
            existing = json.load(f)
    except Exception:
        existing = []
    existing.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(existing, f, indent=2)

def run_checks(os_type):
    check_flow = {
        "windows": [
            ("Disk Encryption", disk_win),
            ("OS Update Status", os_win),
            ("Sleep Settings",  sleep_win),
            ("Antivirus Status", av_win)
        ],
        "linux": [
            ("Disk Encryption", disk_linux),
            ("OS Update Status", os_linux),
            ("Sleep Settings",  sleep_linux),
            ("Antivirus Status", av_linux)
        ],
        "macos": [
            ("Disk Encryption", disk_mac),
            ("OS Update Status", os_mac),
            ("Sleep Settings",  sleep_mac),
            ("Antivirus Status", av_mac)
        ]
    }

    if os_type not in check_flow:
        print(f"❌ Unsupported OS: {os_type}")
        return {}

    results = {}
    for label, check_func in check_flow[os_type]:
        print(f"🔧 {label}:")
        try:
            result = check_func()
            results[label] = result

            # --- Custom block for Disk Encryption ---
            if label == "Disk Encryption" and isinstance(result, dict):
                status = result.get("status")
                unenc  = result.get("unencrypted", [])
                msg    = result.get("message", "")
                if status == "Pass":
                    print(f"✅ {label} status: Pass\n")
                else:
                    print(f"❌ {label} status: Fail")
                    if unenc:
                        print(f"  Unencrypted: {', '.join(unenc)}")
                    print(f"  ⚠ {msg}\n")
                continue

            # -----------------------------------------

            # Boolean pass/fail
            if isinstance(result, bool):
                if result:
                    print(f"✅ {label} status: Pass\n")

            # Dict-based status
            elif isinstance(result, dict):
                st = result.get("status")
                if st == "Pass":
                    print(f"✅ {label} status: Pass\n")

                elif st == "Fail":
                    # OS Update specific
                    if "total" in result:
                        tot  = result["total"]
                        kern = result["kernel"]
                        sev  = result["severity"]
                        print(f"❌ {label}: {tot} updates ({kern} kernel) [{sev}]")
                        # top 5
                        for pkg in result["details"][:5]:
                            print(f"  • {pkg}")
                        more = tot - 5
                        if more > 0:
                            print(f"  …and {more} more")
                        print()
                    else:
                        # generic fail
                        sev = result.get("severity", "Unknown")
                        print(f"❌ {label} status: Fail ({sev})\n")

                elif st == "Error":
                    print(f"⚠️ {label} check failed: {result.get('message')}\n")

                else:  # Info or other
                    print(f"ℹ️ {label}: {result.get('message','')}\n")

            # Fallback for plain strings
            else:
                print(f"📋 {label}: {result}\n")

        except Exception as e:
            results[label] = {"status": "Error", "message": str(e)}
            print(f"⚠️ Exception: {e}\n")

    return results

def run_sysshield(silent=True):
    pid_file = Path("sysshield.pid")
    pid_file.write_text(str(os.getpid()))  # ← write PID here

    if not silent:
        boot_banner()
    os_type   = load_cached_os()
    timestamp = datetime.now().isoformat()
    results   = run_checks(os_type)
    log_results(timestamp, os_type, results)

    with open("sysshield_heartbeat.txt", "a") as f:
        f.write(f"Daemon run at {datetime.now()}\n")
    return results

def daemonize():
    pid_file = Path("sysshield.pid")

    if pid_file.exists():
        print("🛡️ SysShield daemon already running.")
        return

    def remove_pid():
        if pid_file.exists():
            pid_file.unlink()
    atexit.register(remove_pid)

    # Spawn background instance with --run
    if platform.system() == "Windows":
        subprocess.Popen(["pythonw", __file__, "--run"], creationflags=subprocess.DETACHED_PROCESS)
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        subprocess.Popen([sys.executable, __file__, "--run"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("❌ Unsupported platform for daemonization.")
        return

    pid_file.write_text(str(os.getpid()))
    print("✅ SysShield daemon started.")

    sys.exit()

if __name__ == "__main__":
    if "--stop" in sys.argv:
        pid_file = Path("sysshield.pid")
        if pid_file.exists():
            pid = int(pid_file.read_text())
            try:
                os.kill(pid, 9)
                print("🛑 SysShield daemon stopped.")
            except Exception as e:
                print(f"⚠️ Failed to stop daemon: {e}")
            pid_file.unlink()
        else:
            print("ℹ️ No daemon running.")
        sys.exit()

    elif "--run" in sys.argv:
        run_sysshield_loop()

    else:
        daemonize()      # Launch background daemon