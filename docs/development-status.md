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

**Verified in this test:** launching/controlling the receiver through the GUI and successful mirroring with an already registered iPad. **Not independently established by these screenshots:** stopping the current session from the GUI, first-time PIN enrollment through the GUI, audible sound, or reproducibility on other PCs. No personal screenshot or machine-specific file path is committed to this repository.

## GUI features still needing end-to-end testing

- PySide6 window; successfully started the UxPlay receiver for the observed mirroring session; stopping needs separate confirmation.
- Reads the local registry internally and hides device identifiers from the interface.
- Dedicated new-device PIN pairing mode, count of registered devices and connection status.
- Audio enable/disable setting applies when the receiver starts, **not during streaming**.
- 11 unit tests passed in the user's Windows environment in the prior version and can be rerun after replacing the test-only public key fixture.

**Successful GUI startup and mirroring of a previously registered device are now observed.** GUI stop, new-device PIN enrollment, multi-display behavior and error recovery still need separate tests on Windows.

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
