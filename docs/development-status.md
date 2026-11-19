# Development status — v0.1.1 (2026-11-19)

## Working functionality observed in direct UxPlay tests

- Windows 11 + local UxPlay 1.73.7 source build (modified SRP proof length) connected to an iPad.
- A registered iPad reconnected without repeated PIN entry when the same persistent key/registry were used.
- Video, audio and perceived A/V synchronization worked with default `-vsync` behavior.
- Current iPad screen mirroring has acceptable observed Apple Pencil latency for the intended workflow; no latency tuning in this version.

## GUI implementation included but needing end-to-end testing

- PySide6 window; starts/stops its own UxPlay child process.
- Reads the local registry internally and hides device identifiers from the interface.
- Dedicated new-device PIN pairing mode, count of registered devices and connection status.
- Audio enable/disable setting applies when the receiver starts, **not during streaming**.
- 11 unit tests passed in the user's Windows environment in the prior version and can be rerun after replacing the test-only public key fixture.

**A successful direct UxPlay run is not the same as verified end-to-end GUI operation.** GUI start/stop, PIN enrollment, multi-display behavior and error recovery remain to be tested on Windows.

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
