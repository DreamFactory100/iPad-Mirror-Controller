"""Launch only our UxPlay process. Never kill unrelated OS processes."""

from __future__ import annotations

import re
import secrets
from pathlib import Path

from PySide6.QtCore import QObject, QProcess, QProcessEnvironment, Signal

from .command import build_uxplay_args
from .settings import Settings

_PIN_RE = re.compile(r'CLIENT MUST NOW ENTER PIN\s*=\s*"?(\d{4})')


class UxPlayManager(QObject):
    status_changed = Signal(str)
    event = Signal(str)
    pin_requested = Signal(str)
    registration_changed = Signal()
    busy_changed = Signal(bool)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.started.connect(self._started)
        self.process.readyReadStandardOutput.connect(self._read_output)
        self.process.errorOccurred.connect(self._error)
        self.process.finished.connect(self._finished)
        self._buffer = ""
        self._stop_requested = False
        self.pairing_mode = False
        self._startup_pin: str | None = None

    def is_running(self) -> bool:
        return self.process.state() != QProcess.ProcessState.NotRunning

    def start(self, settings: Settings, *, pairing_mode: bool, allowed_ids: list[str]) -> None:
        if self.is_running():
            return
        self._stop_requested = False
        self._buffer = ""
        self.pairing_mode = pairing_mode
        path = Path(settings.uxplay_exe)
        self._startup_pin = str(1000 + secrets.randbelow(9000)) if pairing_mode else None
        args = build_uxplay_args(
            settings, pairing_mode=pairing_mode, allowed_ids=allowed_ids,
            pairing_pin=self._startup_pin,
        )
        env = QProcessEnvironment.systemEnvironment()
        ucrt_bin = Path("C:/msys64/ucrt64/bin")
        env.insert("PATH", str(ucrt_bin) + ";" + env.value("PATH", ""))
        gst_plugins = Path("C:/msys64/ucrt64/lib/gstreamer-1.0")
        if gst_plugins.is_dir():
            env.insert("GST_PLUGIN_SYSTEM_PATH_1_0", str(gst_plugins))
        self.process.setProcessEnvironment(env)
        self.process.setProgram(str(path))
        self.process.setArguments(args)
        self.process.setWorkingDirectory(str(path.parent.parent))
        self.status_changed.emit("PIN 등록 모드 시작 중" if pairing_mode else "서버 시작 중")
        self.process.start()

    def stop(self) -> None:
        if not self.is_running():
            return
        self._stop_requested = True
        self.status_changed.emit("서버 종료 중")
        self.process.terminate()
        if not self.process.waitForFinished(1800):
            self.process.kill()
            self.process.waitForFinished(1500)

    def _started(self) -> None:
        self.busy_changed.emit(True)
        self.event.emit("PIN 등록 모드 시작" if self.pairing_mode else "미러링 서버 시작")
        if self._startup_pin:
            self.pin_requested.emit(self._startup_pin)

    def _read_output(self) -> None:
        data = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        self._buffer += data
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._handle_line(line.strip())
        if len(self._buffer) > 16000:
            self._buffer = self._buffer[-2000:]

    def _handle_line(self, line: str) -> None:
        pin = _PIN_RE.search(line)
        if pin:
            self.pin_requested.emit(pin.group(1))
            self.event.emit("iPad 최초 인증 PIN 표시")
        if "Initialized server socket" in line:
            self.status_changed.emit("PIN 등록 대기 중" if self.pairing_mode else "iPad 연결 대기 중")
        elif "Client Authentication Failure" in line or "Client authentication failure" in line:
            self.status_changed.emit("인증 오류 — 연결 확인 필요")
            self.event.emit("인증 실패")
        elif "registered new client:" in line:
            self.registration_changed.emit()
            self.event.emit("새 iPad 등록 성공")
        elif "connection request from" in line:
            self.status_changed.emit("iPad 연결됨")
            self.pin_requested.emit("")
        elif "Begin streaming to GStreamer video pipeline" in line:
            self.status_changed.emit("화면 미러링 중")
            self.event.emit("미러링 시작")
        elif "raop_rtp_mirror->running is no longer true" in line or "lost connection with client" in line:
            self.status_changed.emit("연결 종료 — 다시 연결 대기")
            self.event.emit("연결 종료")
        # All other lines (IP, device IDs, keys, names) remain unshown.

    def _error(self, error: QProcess.ProcessError) -> None:
        if error == QProcess.ProcessError.FailedToStart:
            self.status_changed.emit("실행 실패 — 파일 경로 확인")
            self.event.emit("UxPlay 시작 실패")

    def _finished(self, exit_code: int, _status: QProcess.ExitStatus) -> None:
        self.busy_changed.emit(False)
        self.pin_requested.emit("")
        self._startup_pin = None
        self.status_changed.emit("서버 중지됨" if self._stop_requested else "서버 종료됨")
        self.event.emit("UxPlay 프로세스 종료")
