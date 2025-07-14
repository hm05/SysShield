# disk_check.py
# 🛡️ SysShield System Utility
# This file is part of the SysShield project
# Developed by Harsh Murjani
import subprocess

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
        if "crypto_LUKS" in result.stdout:
            return True
        else:
            print("❌ Disk Encryption status: LUKS not detected — disk may be unencrypted.")
            return False
    except Exception as e:
        print(f"⚠️ Disk Encryption check failed: {e}")
        return False

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
