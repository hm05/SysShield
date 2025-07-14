# <div align="center">SysShield</div>

**SysShield** is a System Security application software designed for cross platform installation and usage.

|   | Platform | Tested on |
| - | -------- | --------- |
| 1 | Windows  |           |
| 2 | Linux    |           |
| 3 | MacOS    |           |

## <div align="center">🚀 Features 🚀</div>

- **SysShield** provides a very elegant and interactive user interface to check and manage the system health and issues.
- The user can check the security of the disks.
- Check for system updates.
- Antivirus status.
- System sleep settings.

## <div align="center">⚙️ Installation and Setup ⚙️</div>

## <div align="center">📁 Application Structure 📁</div>
The application is divided into 3 parts
- Client Utility
- Client Dashboard
- Backend

The file structure is 
SysShield/
├── client/           # System Utility
│   ├── __init__.py
│   ├── disk_check.py
│   ├── os_check.py
│   ├── sleep_check.py
│   └── antivirus_check.py
├── backend/          # Backend Server
│   ├── main.py
│   ├── models.py
│   └── database/
├── dashboard/        # Admin Dashboard
│   └── src/
├── application/      # Application Package
│   ├── sysshield.exe
│   ├── sysshield.dmg
│   └── sysshield.deb

## <div align="center">ℹ️ About Application ℹ️</div>
Version 1.0.0 <br>
Developed by [Harsh Murjani](https://github.com/hm05) <br>
> [!NOTE]
> This project is a part of hiring assignment assigned by [Solsphere AI](https://solsphere.ai/)
