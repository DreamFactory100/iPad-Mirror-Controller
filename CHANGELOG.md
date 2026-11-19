# Changelog

## v0.1.1 — development snapshot (2026-11-19)

- Removed the manual AirPlay Device ID input from the GUI.
- Added local registered-device discovery and an explicit new-device PIN enrollment mode.
- Kept the previously verified receiver configuration (default audio/video synchronization).
- Preserved modular separation of GUI, settings, pairing registry and UxPlay process management.
- Added automated unit coverage for registration formats and generated command arguments (11 cases).
- Prepared a separate GitHub-safe snapshot: replaced a real paired-device **test public key** with a synthetic fixture. **No application runtime logic was modified for this snapshot.**
- Added repository-facing documentation about attribution, privacy, reproducibility and pending verification.

## v0.1.0 — initial GUI prototype

- First PySide6 Windows window and basic UxPlay server start/stop support.
- Configurable executable and local PIN key/registry paths.
- Audio enable/disable selection at server start.

> A change listed here is not proof of end-to-end Windows GUI validation. See [development status](docs/development-status.md).
