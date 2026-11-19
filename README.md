# iPad Mirror Controller

**Windows GUI for managing an existing UxPlay AirPlay receiver**  
**Version:** `v0.1.1` · **Status:** source-code preview / development prototype (not an installer)

> 한국어: iPad 화면을 Windows PC에 미러링하는 UxPlay 엔진을 GUI에서 실행·중단하고, 최초 PIN 등록과 기존 기기의 자동 재연결을 관리하기 위한 개인 개발 프로젝트입니다. 아직 일반 사용자용 설치 프로그램이 아닙니다.

## Project overview

This is an independently maintained **controller/front-end**, not a new AirPlay protocol implementation. Its core purpose is to make a separately installed [UxPlay](https://github.com/FDH2/UxPlay) receiver more convenient to use for presentations, teaching and screen demonstrations.

**Project maintainer:** [DreamFactory100](https://github.com/DreamFactory100) (GitHub account; public author credit can be updated before release). Development was carried out with AI-assisted coding and iterative local tests. Credit for UxPlay and other dependencies belongs to their respective authors.

### Implemented in v0.1.1

- Start or stop **the UxPlay process started by this GUI**.
- Read locally registered iPads without manually entering an AirPlay device ID.
- Use a persistent key and UxPlay registration file for previously paired devices.
- Provide a separate, user-confirmed **new device registration** mode with a four-digit PIN.
- Select audio enabled/disabled **before server startup**.
- Display limited connection status and a privacy-conscious in-app event log.
- Keep default A/V synchronization (the earlier `-vsync no` option is not used).
- The developer uses a local Windows desktop shortcut; **a public-branded icon, shortcut and portable installer are not included**.

### Not implemented yet

Live mute/volume control, a system-tray controller, full-screen/window management, an independent installer and standalone dependency packaging. Those items are **planned**, not current features.

## Verification status

| Component | Status |
| --- | --- |
| UxPlay mirroring, audio and A/V sync | Worked on the developer's Windows 11/iPad test environment when run directly |
| One-time PIN pairing and reconnection | Worked with a locally built, adjusted UxPlay receiver |
| PySide6 GUI v0.1.1 | Code and automated tests passed; full start/stop and pairing workflow **not yet verified end-to-end** on Windows |
| Automated tests | 11 Python unit tests passed on the developer's Windows PC; can be rerun below |
| Portable Windows installer | Not available |

**Important reproducibility note:** the successful receiver used a **locally modified UxPlay v1.73.7 build**, correcting the expected SRP proof length in `lib/raop_handlers.h` from 64 to 20 bytes. This repository does **not** ship UxPlay, its patch, MSYS2, GStreamer or Apple's Bonjour components. An unmodified UxPlay v1.73.7 build may therefore behave differently during PIN pairing. For future redistribution, the compatible upstream version/patch and corresponding license obligations must be documented and tested.

## Development setup (Windows, not a turnkey install)

**Prerequisites:** Windows 11, Python 3.12, a *separately installed and working* UxPlay executable with its dependencies and an appropriately configured trusted local network. The current code expects a Windows/MSYS2 UCRT64-style environment for automatic discovery; other installations may need manual path configuration. For practical installation constraints and safe reproduction steps see [Try it on Windows](docs/TRY_IT_ON_WINDOWS.md).

```powershell
# Run from the folder containing main.py
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" ".\main.py"
```

After launching, verify that **UxPlay 실행 파일**, **PIN 인증키 파일** and **등록 정보 파일** refer to your own local files. Do not copy another person's pairing secrets.

### Basic operation

1. For a previously registered iPad, press **서버 시작** and select the UxPlay receiver in iPad **화면 미러링**. A new PIN is normally unnecessary when valid local registration data and the same receiver key are used.
2. For a new iPad, choose **새 iPad 등록 (PIN)** *only on a trusted private network*, enter the displayed PIN on that iPad, then stop enrollment and restart the server in normal mode.
3. Press **서버 중단** to stop the receiver process launched by the GUI.

**Security behavior:** normal mode restricts connections to device IDs read internally from the local UxPlay registry. Enrollment mode temporarily permits new devices to attempt PIN pairing on the local network; return to normal mode afterward. Pairing keys/registration state are local runtime data, not repository files.

### Run tests

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -v
```

## Repository layout

```text
app/core/                 # Configuration, registration, command construction and process control
app/ui/                   # PySide6 GUI
docs/                     # Development status and security notes
tests/                    # Synthetic test fixtures and unit tests
main.py                   # Program entry point
requirements.txt          # GUI dependency
```

## Privacy and source control

No live receiver private key, paired-device registry, local settings, full connection logs or real device IDs are intentionally included. Tests use **synthetic** key and device-ID fixtures. Keep `.pem`, `.register` and `settings.local.json` out of commits. See [Security and privacy](docs/SECURITY_AND_PRIVACY.md). Treat `.gitignore` as a safeguard, **not** a replacement for reviewing the files you stage.

## Credits, licensing and trademarks

- Receiver engine: [UxPlay](https://github.com/FDH2/UxPlay) — a separate open-source project under GPLv3. Its source is not included here.
- Desktop GUI: [PySide6 / Qt for Python](https://doc.qt.io/qtforpython-6/) — subject to its applicable open-source/commercial license terms.
- GStreamer, Bonjour and other runtime components are separately supplied and have their own terms.
- **The original controller code does not yet have an explicit license.** Public visibility by itself does not grant broad permission to reuse, modify or redistribute the code. Before inviting others to use, modify or redistribute it, the maintainer must choose and publish an appropriate license; see [Publication checklist](docs/PUBLICATION_CHECKLIST.md).
- `iPad`, `AirPlay` and Apple imagery are trademarks of Apple Inc. This is an **unofficial, independent project** and is not affiliated with or endorsed by Apple. The developer’s locally used icon contains Apple-branded imagery and has been **excluded** from this public-candidate archive; a new unbranded logo is needed for general release.

See [Third-party notices](THIRD_PARTY_NOTICES.md) and [Development status](docs/development-status.md). This repository is a **development snapshot**, not a finished product or official Apple application. See [Getting started](docs/TRY_IT_ON_WINDOWS.md) for the present prerequisites and limitations.
