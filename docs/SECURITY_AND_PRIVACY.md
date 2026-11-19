# Security and privacy — development snapshot

## Local data

The GUI uses local UxPlay files to retain PIN pairing across sessions. A user's `.pem` key file and `.register` paired-device registry are **personal runtime data**, not source code. The registry can contain device identifiers and public keys, and connection logs may reveal device names and addresses.

**Never commit or publish:** `settings.local.json`, `.pem` or `.register` files, private/public pairing records from actual devices, personal IP/MAC addresses, active PIN screenshots, unredacted diagnostics, or raw network traces.

Tests in this GitHub-ready copy use synthetic identifiers and a synthetic 32-byte base64 fixture. These values do not identify a real device.

## Connection model

- Normal mode builds a UxPlay allowlist from locally registered devices and uses PIN key/registry persistence.
- Explicit PIN-enrollment mode intentionally relaxes the device allowlist to accept new pairing attempts, but requires the generated PIN.
- Only pair on a *trusted* private network; do not switch public/hotel networks to Private just to establish mirroring.
- The known Windows setup uses per-program Private-profile, LocalSubnet firewall rules. **This repository does not create, remove, or relax firewall rules.**
- Device IDs are an access-control aid, not a substitute for cryptographic validation. The security of the full system also depends on UxPlay, Windows, network isolation and third-party runtimes.

## Before publishing or distributing

1. Inspect `git status` and `git diff --cached --name-only` before every first commit/release.
2. Check the staged files for local paths, personal names, device IDs, exported logs, private keys and registration data.
3. Keep the current development icon private until Apple trademark/brand permission implications have been assessed.
4. Verify third-party licenses and any bundled executable or SDK terms.
5. Test the installation/GUI on a clean Windows system; the current snapshot is not a standalone installer.

**Security issues:** report privately to the repository maintainer rather than posting real PINs, keys, network addresses or device logs in a public issue.
