# disk_check.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani
import subprocess
import re

def disk_win():
    print("Checking disk encryption on Windows...")
    try:
        result = subprocess.run(["manage-bde", "-status"], capture_output=True, text=True)
        if "Fully Encrypted" in result.stdout:
            return True
        else:
            print("❌ Disk Encryption status: BitLocker is OFF — please enable it using 'manage-bde' or Settings.")
            return False
    except Exception as e:
        print(f"⚠️ Disk Encryption check failed: {e}")
        return False

def disk_linux():
    print("Checking disk encryption on Linux...")
    try:
        result = subprocess.run(["lsblk", "-o", "NAME,FSTYPE"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]
        exclude = ["sr0", "loop", "boot", "efi", "cdrom", "nvme0n1p1"]
        encrypted = []
        unencrypted = []
        notes = []
        severity_map = {}

        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                name_raw, fstype = parts[0], parts[1]
                name = re.sub(r'[└─├─]', '', name_raw)

                if not fstype:
                    continue
                if fstype == "crypto_LUKS":
                    encrypted.append(name)
                    continue

                # Assign severity flags
                if "swap" in name.lower():
                    severity = "Medium"
                elif "root" in name.lower() or name.endswith("p3"):
                    severity = "High"
                elif any(tag in name.lower() for tag in exclude):
                    severity = "Low"
                else:
                    severity = "Medium"

                unencrypted.append(name)
                severity_map[name] = severity

        # Check fstab and crypttab
        try:
            crypttab = open("/etc/crypttab").read()
        except Exception:
            crypttab = ""
        try:
            fstab = open("/etc/fstab").read()
        except Exception:
            fstab = ""

        for disk in unencrypted:
            if disk not in crypttab and disk not in fstab:
                notes.append(f"{disk} not found in /etc/crypttab or fstab")

        print(f"❌ Unencrypted partitions detected: {', '.join(unencrypted)}")
        for note in notes:
            print(f"⚠️ {note}")

        return {
            "status": "Pass" if not unencrypted else "Fail",
            "unencrypted": unencrypted,
            "excluded": [d for d in exclude if any(d in u.lower() for u in unencrypted)],
            "notes": notes,
            "severity": severity_map
        }

    except Exception as e:
        print(f"⚠️ Disk Encryption check failed: {e}")
        return {
            "status": "Error",
            "message": str(e)
        }

def disk_mac():
    print("Checking disk encryption on macOS...")
    try:
        result = subprocess.run(["fdesetup", "status"], capture_output=True, text=True)
        if "FileVault is On" in result.stdout:
            return True
        else:
            print("❌ Disk Encryption status: FileVault is OFF — please enable it in System Settings.")
            return False
    except Exception as e:
        print(f"⚠️ Disk Encryption check failed: {e}")
        return False
