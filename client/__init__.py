# __init__.py
# 🛡️ SysShield System Utility
# Developed by Harsh Murjani

__version__ = "1.0.0"
__author__ = "Harsh Murjani"

import platform
import json
from datetime import datetime

from disk_check import disk_win, disk_linux, disk_mac
from os_check   import os_win,    os_linux,    os_mac
from sleep_check   import sleep_win,   sleep_linux,   sleep_mac
from antivirus_check import av_win,    av_linux,    av_mac

CACHE_PATH = "os_cache.json"
LOG_PATH   = "sysshield_logs.json"

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
                notes  = result.get("notes", [])
                if status == "Pass":
                    print(f"✅ {label} status: Pass\n")
                else:
                    print(f"❌ {label} status: Fail")
                    print(f"  Unencrypted: {', '.join(unenc)}")
                    for note in notes:
                        print(f"  ⚠ {note}")
                    print()
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

def run_sysshield():
    boot_banner()
    os_type   = load_cached_os()
    timestamp = datetime.now().isoformat()
    results   = run_checks(os_type)
    log_results(timestamp, os_type, results)
    return results

if __name__ == "__main__":
    run_sysshield()
