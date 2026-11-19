# Development status — v0.1.1 (2026-11-19)

## Working functionality observed in direct UxPlay tests

- Windows 11 + local UxPlay 1.73.7 source build (modified SRP proof length) connected to an iPad.
- A registered iPad reconnected without repeated PIN entry when the same persistent key/registry were used.
- Video, audio and perceived A/V synchronization worked with default `-vsync` behavior.
- Current iPad screen mirroring has acceptable observed Apple Pencil latency for the intended workflow; no latency tuning in this version.

## GUI real-device validation — 2026-11-19

The developer supplied screenshots from the installed Windows 11 GUI v0.1.1 showing:
- The GUI reported **화면 미러링 중** (Screen Mirroring Active).
- One previously PIN-authorized iPad was recognized in the GUI.
- A mirrored presentation slide was displayed in the Windows **Direct3D11 renderer** window.
- The GUI event log recorded the beginning of mirroring.

**Verified by the supplied screenshots:** launching/controlling the receiver through the GUI and successful mirroring with an already registered iPad. **Additionally confirmed by the developer's follow-up functional test:** pressing GUI **서버 중단** (Stop Server) closed the stream and returned the GUI to its stopped state; starting again enabled PIN-free reconnection of the registered iPad. **Follow-up test reported by the developer on 2026-11-19:** GUI **새 iPad 등록 (PIN)** (Register New iPad) entered enrollment mode and displayed a four-digit PIN, as shown in two screenshots. The developer reports successfully pairing a different device. The screenshots themselves establish the enrollment dialog and PIN-display stage, not independently the completed pairing. **Still not verified:** audio specifically through GUI and reproducibility on another PC. No personal screenshot or machine-specific file path is committed to this repository.

## GUI features still needing end-to-end testing

- PySide6 window; GUI start, stop, and PIN-free reconnection of the previously registered iPad confirmed by the developer.
- Reads the local registry internally and hides device identifiers from the interface.
- New-device PIN pairing mode was used successfully with a second device according to the developer's functional test; screenshots show enrollment mode and PIN generation. The registered-device count and other connection behaviors remain as implemented.
- Audio enable/disable setting applies when the receiver starts, **not during streaming**.
- 11 unit tests passed in the user's Windows environment in the prior version and can be rerun after replacing the test-only public key fixture.

**GUI startup, mirroring, stop/restart without repeated PIN, and registration of a different device (developer-reported) have now been tested on the development PC.** Multi-display behavior, GUI audio and error recovery still need separate checks.

## Planned (not implemented)

- Real-time UxPlay-only mute/unmute and volume controls.
- System-tray controls, fullscreen/window management, single-instance enforcement.
- Package dependency management and a Windows installer independent of MSYS2.
- Automated integration tests and tests on other Windows PCs.
- Public-facing documentation/screenshots that do not expose personal information.

## Known constraints

- Expects a separately installed and functional UxPlay receiver and related dependencies.
- Auto-discovery uses `C:/msys64/...`; it may need adaptation for other PCs.
- Developer observed a Windows desktop click/overlay issue and a Bonjour LSA module warning during system testing; **causality not established**. Do not claim the prototype resolves either issue.
- The privately used icon contains Apple branding and is excluded from this public candidate. Replace with unbranded artwork for the eventual public release.

## Repository backup decisions

- App runtime modules, `main.py`, and the v0.1.1 implementation **are unchanged** from the working development snapshot.
- Test public-key fixture only: substituted a synthetic value in `tests/test_settings.py` to prevent publication of a real device registration public key.
- Added documentation and strengthened `.gitignore`. The developer’s local icon remains unchanged; it is omitted only from the public-candidate package.
