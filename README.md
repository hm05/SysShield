# <div align="center">SysShield</div>

**SysShield** is a System Security application software designed for cross platform installation and usage.

|   | Platform | Tested on |
| - | -------- | --------- |
| 1 | Windows  | Windows 11 Home Single Language (24H2) |
| 2 | Linux    | Kali 2025.1 rolling |
| 3 | MacOS    | MacOS Sequoia v15.5 |

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
```
SysShield/
├── README.md                 # Project Documentation
├── requirements.txt
├── .gitignore
├── os_cache.json
├── sysshield_logs.json
├── sysshield_heartbeat.txt
├── client/                   # System Utility
│   ├── cert.pem
│   ├── __init__.py
│   ├── disk_check.py
│   ├── os_check.py
│   ├── sleep_check.py
│   └── antivirus_check.py
```

## <div align="center">🧑‍🎨 Figma Design 🧑‍🎨</div>


[SysShield Figma Design](https://www.figma.com/proto/ChzaoxofeVl2hSaO4ZWpMX/SysShield-UI?node-id=1-2&p=f&t=DRPElSUJT1yOtfO4-1&scaling=scale-down-width&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=1%3A2)
**Variables Value**
Fonts:Kodchasan
Border Radius: 50px
Background Color: #FBFAF5
Secondary Background: #DBE7F3
Graph Border: #018FC7
Green: #00B00
Red: #EA324C

## <div align="center">ℹ️ About Application ℹ️</div>
Version 1.0.0 <br>
Developed by [Harsh Murjani](https://github.com/hm05) <br>
> [!NOTE]
> This project is a part of hiring assignment assigned by [Solsphere AI](https://solsphere.ai/)
