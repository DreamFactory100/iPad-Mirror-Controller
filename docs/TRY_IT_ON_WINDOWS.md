# Try iPad Mirror Controller on Windows (source-code prototype)

This document describes **what is currently required to experiment**. It is not a one-click setup. The GUI controls a separately prepared UxPlay receiver; it does not implement AirPlay itself.

## What you need

- A Windows 11 PC and an iPad on a **trusted** local network, ideally the same Wi-Fi/LAN segment.
- Python 3.12 and PySide6 (installed via the project's `requirements.txt`).
- [UxPlay](https://github.com/FDH2/UxPlay) installed/built separately for Windows, including its runtime libraries and compatible service discovery (e.g. GStreamer, MSYS2 UCRT64 and appropriate mDNS/Bonjour support as documented by upstream).
- A UxPlay build that actually supports successful `-pin` + `-reg` pairing with your iPad. **Do not assume that any arbitrary UxPlay executable will work.**

The developer used UxPlay **v1.73.7** with a local source adjustment in `lib/raop_handlers.h` to accept a 20-byte SRP proof rather than 64 bytes, followed by a rebuild. That locally tested adjustment is **not bundled or promised to work elsewhere**. Prefer the maintained upstream version if it is compatible and verify its own build instructions. If experimenting with the older build, preserve the original source and understand that changing a length check does not guarantee successful cryptographic pairing. Do not bypass SRP verification.

## Run the GUI

Open **Windows PowerShell** in the cloned project folder:

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" ".\main.py"
```

In the GUI, set these paths for **your own PC**:

- **UxPlay 실행 파일** — a working `uxplay.exe` built or installed on your computer.
- **PIN 인증키 파일** — a local private key path, generated and reused by UxPlay as appropriate.
- **등록 정보 파일** — a local paired-device registry path, reused alongside the original key.

The development prototype currently prepends `C:/msys64/ucrt64/bin` to the UxPlay subprocess PATH and auto-discovers a source build under `C:/msys64/home/<user>/projects/UxPlay/build`. A different layout may require developer changes; this is **not yet a generally portable setup**.

## Pairing and normal use

1. Use **새 iPad 등록 (PIN)** on a trusted private network and enter the displayed PIN on the iPad. The iPad itself selects the receiver in its screen-mirroring menu.
2. After pairing, stop enrollment. Use **서버 시작** for the registered iPad; an existing key + registry normally allows reconnection without another PIN.
3. Use **서버 중단** to stop the UxPlay instance launched by the GUI.
4. **오디오** is a start-time option; live mute/volume control is not implemented in v0.1.1.

## Network and security

- Keep Windows Firewall enabled. On trusted local networks, allow only the necessary per-program/local-subnet traffic; never disable the firewall or Windows LSA protections just to make mirroring work.
- Do not set public/hotel Wi-Fi to the Private network profile solely to permit AirPlay.
- **Never upload** `.pem`, `.register`, `settings.local.json`, Wi-Fi credentials, live PINs or raw logs to an issue or repository.
- Some older Bonjour components may trigger a Windows LSA blocking notification. This is not a reason to disable LSA protection. Prefer modern, supported service-discovery configurations where possible.
- A prior desktop click issue occurred during development, but its cause was not established. It is not known to be caused by this application or fixed by this release.

## Tests

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -v
```

The automated tests cover selected configuration and argument-building behavior. They **do not** prove full end-to-end Windows/iPad operation or compatibility on other hardware.

## Not included

UxPlay executable/source, patched UxPlay sources, GStreamer, MSYS2, Bonjour, private pairing files, a redistributable installer, and the developer's Apple-branded local icon. Refer to [UxPlay upstream documentation](https://github.com/FDH2/UxPlay) for the upstream engine and licensing conditions.
