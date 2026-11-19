# Try iPad Mirror Controller on Windows (source-code prototype)

**Status: development preview, not a one-click installer.** This controller starts a **separately prepared UxPlay receiver**. It does not implement the AirPlay protocol or bundle UxPlay, Windows runtime libraries, or pairing credentials.

These instructions distinguish (a) the developer's **tested** setup from (b) upstream options that have **not** been tested with this GUI on a clean PC. No system-wide security protection needs to be disabled.

## 1. Requirements and compatibility

- Windows 11 (64-bit x86-64 tested), an iPad/iPhone and a **trusted private** local Wi-Fi/LAN.
- Python 3.12 and a terminal capable of running PowerShell.
- MSYS2 installed in its default location, `C:\msys64`, using the **UCRT64** environment, plus GStreamer and a working `uxplay.exe`.
- Working local-network service discovery (Bonjour for the developer's older UxPlay 1.73.7 build).
- Sufficient space to install developer tools. **No installer or bundled third-party runtime** is provided by this repository.

**Version distinction:**

| UxPlay setup | Discovery and pairing | Status with this GUI |
| --- | --- | --- |
| Locally built **1.73.7** with the developer's specific SRP proof-length adjustment | Bonjour SDK/service; persistent `-key` and `-reg` | **Tested** on the developer's Windows 11 PC |
| Upstream **1.74 and later** (if available in the selected branch/release) | Upstream added a built-in mDNS option, reducing Bonjour dependency; use upstream documentation | **Not tested** with this GUI |
| Unmodified older releases or arbitrary third-party binaries | PIN/SRP behavior and codecs may vary | **Not guaranteed** |

The developer's 1.73.7 source adjustment was `lib/raop_handlers.h`: changing the expected SRP proof buffer length from **64** to **20** bytes, then rebuilding. This describes one observed compatibility fix; **do not treat it as a universal patch**, suppress cryptographic verification, or apply it blindly to newer releases. This repository deliberately does not ship that modified UxPlay binary or source. Prefer a maintained upstream version when compatible.

Upstream reference: [FDH2/UxPlay Windows build and operating instructions](https://github.com/FDH2/UxPlay#building-uxplay-on-microsoft-windows-using-msys2-with-the-mingw-64-compiler).

## 2. Prepare MSYS2 and the UxPlay runtime

Install [MSYS2](https://www.msys2.org/) and open its **MSYS2 UCRT64** terminal (not the plain MSYS terminal). Commands below run **inside UCRT64**, not PowerShell.

Update the package environment first. If the updater requests closing and reopening the terminal, do that and rerun the update.

```bash
pacman -Syu
```

Install the compiler, CMake, Ninja, Git and the libraries required by the upstream Windows build:

```bash
pacman -S --needed git mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-cmake mingw-w64-ucrt-x86_64-ninja
pacman -S --needed mingw-w64-ucrt-x86_64-libplist mingw-w64-ucrt-x86_64-gstreamer mingw-w64-ucrt-x86_64-gst-plugins-base
pacman -S --needed mingw-w64-ucrt-x86_64-gst-libav mingw-w64-ucrt-x86_64-gst-plugins-good mingw-w64-ucrt-x86_64-gst-plugins-bad
```

The **older, tested 1.73.7 configuration** additionally used Apple's Bonjour SDK/service to advertise the receiver. Install the appropriate Bonjour components from legitimate sources according to UxPlay's documentation; do not obtain random DLLs or disable Windows Local Security Authority (LSA) protection to address blocked components. UxPlay 1.74's newer internal-mDNS approach is worth testing separately but **not a confirmed drop-in replacement** for this prototype.

Fetch the official UxPlay source and compile:

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/FDH2/UxPlay.git
cd UxPlay
cmake -S . -B build -G Ninja
cmake --build build
./build/uxplay.exe -h
```

**Important:** the command above fetches the **current upstream source**, not the developer's exact historical build. A successful compile is **not** proof that PIN pairing works with this GUI. If you need to reproduce the older version exactly, select the corresponding source revision/tag first and address the Bonjour/SRP compatibility separately; do not assume `git clone` alone reproduces the tested setup.

The resulting executable should be at `~/projects/UxPlay/build/uxplay.exe`, which usually corresponds to a Windows path such as `C:\msys64\home\<your-msys-username>\projects\UxPlay\build\uxplay.exe`.

Check that the GStreamer elements required by **this GUI's current, fixed video pipeline** are present:

```bash
gst-inspect-1.0 avdec_h264
gst-inspect-1.0 d3d11videosink
```

The GUI currently supplies `-vd avdec_h264 -vs d3d11videosink` and assumes MSYS2 libraries under `C:\msys64\ucrt64`. If either element is absent, fix the GStreamer installation first. Other paths, architectures, codecs or renderers may require future code changes.

## 3. Download and start the GUI (PowerShell)

From [this repository](https://github.com/DreamFactory100/iPad-Mirror-Controller), use **Code → Download ZIP** and extract it, or clone it with Git. Open **PowerShell in the extracted project folder** (the folder containing `main.py`).

```powershell
py -3.12 --version
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" ".\main.py"
```

If `py -3.12` is unavailable, install Python 3.12 and check the Windows Python launcher. Do not copy another user's `.venv` directory.

In the GUI, provide the paths for **your own machine**:

| Korean GUI label | English meaning | Expected value |
| --- | --- | --- |
| **UxPlay 실행 파일** | UxPlay Executable | Absolute path to your working `uxplay.exe` |
| **PIN 인증키 파일** | PIN Authentication Key File | Your **own**, persistent local `.pem` path |
| **등록 정보 파일** | Registration File | Your **own**, persistent local `.register` path |
| **수신기 이름** | Receiver Name | A distinctive name to recognize on the iPad |
| **오디오** | Audio | Enabled/disabled **before** starting the receiver |

For a **first-time setup**, choose two new local file paths in a directory where your Windows account has write permission. UxPlay can create the key and registration file when registering the first device. Keep these **same files** for later sessions; don't delete or regenerate the key when a registry already exists. The GUI intentionally refuses a registry without its corresponding key.

This prototype attempts to discover a local build under `C:\msys64\home\...\projects\UxPlay\build`. **Always verify the detected paths**; the private key/registry names shown in the original development environment were personal test filenames, not files you should download from this repository.

## 4. Pair a new device; reconnect normally

1. On a trusted private Wi-Fi/LAN, make sure no UxPlay receiver is already running from the GUI.
2. Press **＋ 새 iPad 등록 (PIN)** (Register New iPad). Confirm the security prompt.
3. On your iPad, open **화면 미러링** (Screen Mirroring) and choose the named receiver. Enter the four-digit PIN **shown in your GUI** if prompted.
4. Confirm that the new device is registered. Press **■ 서버 중단** (Stop Server) to **leave enrollment mode**. The registration file and private key stay on your computer.
5. Press **▶ 서버 시작** (Start Server). Select the receiver again from the iPad. With the **same key and registry**, the previously paired device should normally reconnect without another PIN.
6. Press **■ 서버 중단** to stop the receiver process launched by this controller.

**Security model:** normal mode uses registered device IDs internally to restrict connections. During enrollment, a new local-network client may request PIN pairing. Only use enrollment on a trusted network, and **stop and return to normal mode immediately afterward**. Do not paste a PIN, key, device ID or registration-file contents into a public GitHub issue.

**Audio:** select **서버 시작 시 소리 켜기** (Enable Audio at Server Start) **before** starting. Live mute/volume changes are not supported by v0.1.1. The developer tested audio directly with UxPlay; separate GUI-audio verification on another PC is still pending.

## 5. Safe troubleshooting

| Symptom | First checks |
| --- | --- |
| GUI reports **UxPlay 시작 실패** (UxPlay Start Failed) | Verify executable path, user permissions, MSYS2 UCRT64 installation and required DLLs |
| Receiver absent in iPad **화면 미러링** | Check same private LAN, receiver running, appropriate mDNS/Bonjour service, network isolation and Windows Firewall **per-program** allowance |
| PIN rejected or device fails to register | Check matching UxPlay version, PIN/SRP behavior and writable key/registry paths; do not overwrite existing keys or turn off authentication |
| Video doesn't open | Check `gst-inspect-1.0 avdec_h264` and `gst-inspect-1.0 d3d11videosink`; look for GPU/driver compatibility |
| Previously registered device asks for a new PIN | Confirm the same persistent private key **and** registry file are being used |
| Warning about Bonjour/LSA protection | Do **not** disable Windows LSA protections; investigate supported service-discovery alternatives and legitimate upstream dependencies |

Keep Windows Firewall enabled. Restrict any necessary inbound permissions to the UxPlay executable on a **trusted private network**, ideally local subnet only. Never reclassify a public/hotel network just to bypass restrictions. Do not assume that a Windows warning or unrelated desktop issue was caused by this GUI without evidence.

## 6. Run automated tests (PowerShell)

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -v
```

The 11 Python unit tests passed in the developer's earlier Windows test. The developer also validated GUI startup, mirroring, stop/restart, PIN-free reconnect and registration of another device on their PC. **These results do not establish compatibility on a clean Windows installation.**

## 7. Scope, privacy and third-party ownership

- This repository contains only the original **GUI/controller source**, tests and documentation. It is **not** a UxPlay fork.
- Not bundled: UxPlay binary/source/patch, MSYS2, GStreamer, Bonjour SDK, keys, registered-device IDs, user's settings or an installer.
- Do not commit `.pem`, `.register`, `settings.local.json`, logs, private screen captures or network credentials. Check staged changes even when `.gitignore` is present.
- UxPlay is a separate GPLv3 project; other components have their own licenses. The license for this controller remains **unselected** pending the maintainer's public-release decision.
- This is an independent, unofficial project and is not affiliated with or endorsed by Apple. The developer's Apple-branded personal shortcut icon is **not** part of the published source.

Further details: [Privacy and security](SECURITY_AND_PRIVACY.md) · [Development status](development-status.md) · [Third-party notices](../THIRD_PARTY_NOTICES.md).
