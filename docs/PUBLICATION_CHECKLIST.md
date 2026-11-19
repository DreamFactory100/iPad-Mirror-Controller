# Publication and distribution checklist

**Status:** Public-source *candidate*, **not yet cleared for public end-user use/distribution**. This checklist does not grant a software license.

## Required before an open-source Public release

- [ ] **Choose the controller's own license** and add its complete `LICENSE` file. Without one, GitHub visibility does not grant broad rights to use, modify or redistribute the code. GPL-3.0-only is one potential copyleft choice aligned with UxPlay's GPLv3; other compatible choices are possible for a separate controller. Assess your intended commercial/distribution strategy before granting rights, as existing grants cannot simply be revoked for prior recipients.
- [x] Remove real paired-device identifiers, key material, runtime settings and logs from candidate files; tests use synthetic fixtures.
- [x] Omit the Apple-branded local `.ico` from the public-candidate archive. The original development machine's icon remains unchanged.
- [ ] Pick an original, unbranded icon and decide whether the product name should emphasize compatibility rather than imply Apple endorsement.
- [x] Clearly identify original controller code versus third-party UxPlay and other dependencies.
- [x] Distinguish implemented features from roadmap and direct UxPlay testing from not-yet-performed GUI end-to-end tests.
- [x] Expand the developer-oriented Windows source setup guide with MSYS2/UCRT64 preparation, UxPlay build outline, pairing paths, GUI labels and safe troubleshooting; distinguish tested 1.73.7 from newer untested configurations.

## Recommended before announcing a version for general users

- [x] On the developer's Windows PC: verify GUI launch, mirroring, stop/relaunch, PIN-free reconnection and first-time PIN enrollment of a different device (reported successful by developer; screenshots show the PIN stage).
- [ ] Verify audio via the GUI, desktop interaction, and the full workflow on a clean Windows environment or another PC.
- [ ] Document a reproducible compatible UxPlay version/build or provide a properly licensed installer and dependency package.
- [ ] Test on another Windows computer and iPad and capture redacted screenshots.
- [ ] Check Windows Defender and local-network firewall behavior without broadly disabling system protections.
- [ ] Audit the licenses of any binaries/plugins you eventually distribute (UxPlay GPLv3, GStreamer plugin licenses, Qt/PySide6, Bonjour SDK distribution rights).
- [ ] Add release version, dated notes, support scope and known issues.

**Do not confuse a public source repository with a one-click application download.** This project currently requires substantial manual setup; it is not a prebuilt Windows installable program.
