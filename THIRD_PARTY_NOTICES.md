# Third-party software and trademark notices

This is a **development snapshot** of an independent GUI controller. No third-party binaries are bundled in this GitHub-ready archive.

| Dependency / mark | Upstream or rights holder | Role | Distribution consideration |
| --- | --- | --- | --- |
| [UxPlay](https://github.com/FDH2/UxPlay) | UxPlay contributors | AirPlay receiver engine, separately installed | GPLv3 source and redistribution requirements apply if redistributing the engine or derivatives |
| [PySide6 / Qt for Python](https://doc.qt.io/qtforpython-6/) | Qt contributors / The Qt Company | GUI bindings | Verify applicable LGPL/GPL/commercial license and corresponding obligations for packaging |
| [GStreamer](https://gstreamer.freedesktop.org/) | GStreamer contributors | Audio/video pipeline required by UxPlay | Individual libraries and plugins may have different licenses; review bundled components |
| Apple Bonjour / Bonjour SDK | Apple Inc. | Local service discovery in developer's Windows setup | Separate Apple terms may restrict redistribution; not packaged here |
| iPad / AirPlay names (local developer icon uses Apple symbol) | Apple Inc. | Compatibility descriptions | No Apple emblem is bundled in this public-candidate archive; avoid third-party logo use without applicable rights |

**Scope:** the present repository contains original Python controller code, documentation, and tests only; the Apple-branded local `.ico` is not shipped. No UxPlay code, `uxplay.exe`, the Bonjour SDK, MSYS2 runtime, GStreamer components or private registration material is provided.

**Not a license grant:** this document is an acknowledgement of upstream projects, **not** a substitute for their actual license texts or legal review. The repository's original GUI/controller code is distributed under the [MIT License](LICENSE), copyright (c) 2026 DreamFactory100. This MIT grant **does not change** the terms of UxPlay or other third-party dependencies. Confirm compatibility and attribution requirements before offering a bundled application release.
