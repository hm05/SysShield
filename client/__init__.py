# __init__.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani

__version__ = "1.0.0"
__author__ = "Harsh Murjani"

import platform, requests, json, uuid
from datetime import datetime
from disk_check import disk_win, disk_linux, disk_mac
from os_check import os_win, os_linux, os_mac
from sleep_check import sleep_win, sleep_linux, sleep_mac
from antivirus_check import av_win, av_linux, av_mac

CACHE_PATH = "os_cache.json"
API_URL = "https://localhost:8000/api/system/update"
LOG_PATH = "sysshield_logs.json"
API_KEY = "super-secret-key"

def detect_os():
    return {
        "Windows": "windows",
        "Linux": "linux",
        "Darwin": "macos"
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

def get_mac_address():
    mac = uuid.getnode()
    return ':'.join(['{:02x}'.format((mac >> ele) & 0xff)
                     for ele in range(40, -1, -8)])

def log_results(timestamp, os_type, results):
    entry = {
        "machine_id": get_mac_address(),
        "timestamp": timestamp,
        "os": os_type,
        "results": results
    }
    try:
        with open(LOG_PATH) as f:
            existing = json.load(f)
    except Exception:
        existing = []
    existing.append(entry)
    try:
        response = requests.post(
            API_URL,
            json=entry,
            headers={ "x-api-key": API_KEY },
            verify="cert.pem"
        )
        print("POST status:", response.status_code)
        if response.status_code != 200:
            print("Warning: Server responded with:", response.text)
    except requests.exceptions.RequestException as e:
        print("POST failed:", str(e))
    with open(LOG_PATH, "w") as f:
        json.dump(existing, f, indent=2)

def run_checks(os_type):
    check_flow = {
        "windows": [
            ("Disk Encryption", disk_win),
            ("OS Update Status", os_win),
            ("Sleep Settings", sleep_win),
            ("Antivirus Status", av_win)
        ],
        "linux": [
            ("Disk Encryption", disk_linux),
            ("OS Update Status", os_linux),
            ("Sleep Settings", sleep_linux),
            ("Antivirus Status", av_linux)
        ],
        "macos": [
            ("Disk Encryption", disk_mac),
            ("OS Update Status", os_mac),
            ("Sleep Settings", sleep_mac),
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

            if label == "Disk Encryption" and isinstance(result, dict):
                status = result.get("status")
                unenc = result.get("unencrypted", [])
                msg = result.get("message", "")
                if status == "Pass":
                    print(f"✅ {label} status: Pass\n")
                else:
                    print(f"❌ {label} status: Fail")
                    if unenc:
                        print(f"  Unencrypted: {', '.join(unenc)}")
                    print(f"  ⚠ {msg}\n")
                continue

            if isinstance(result, bool):
                if result:
                    print(f"✅ {label} status: Pass\n")
            elif isinstance(result, dict):
                st = result.get("status")
                if st == "Pass":
                    print(f"✅ {label} status: Pass\n")
                elif st == "Fail":
                    if "total" in result:
                        tot = result["total"]
                        kern = result["kernel"]
                        sev = result["severity"]
                        print(f"❌ {label}: {tot} updates ({kern} kernel) [{sev}]")
                        for pkg in result["details"][:5]:
                            print(f"  • {pkg}")
                        more = tot - 5
                        if more > 0:
                            print(f"  …and {more} more")
                        print()
                    else:
                        sev = result.get("severity", "Unknown")
                        print(f"❌ {label} status: Fail ({sev})\n")
                elif st == "Error":
                    print(f"⚠️ {label} check failed: {result.get('message')}\n")
                else:
                    print(f"ℹ️ {label}: {result.get('message','')}\n")
            else:
                print(f"📋 {label}: {result}\n")
        except Exception as e:
            results[label] = {"status": "Error", "message": str(e)}
            print(f"⚠️ Exception: {e}\n")
    return results

def run_sysshield():
    print("\n🛡️  SysShield Client - v1.0.0")
    print(f"⏱️  Run Time: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    os_type = load_cached_os()
    timestamp = datetime.now().isoformat()
    results = run_checks(os_type)
    log_results(timestamp, os_type, results)

if __name__ == "__main__":
    run_sysshield()