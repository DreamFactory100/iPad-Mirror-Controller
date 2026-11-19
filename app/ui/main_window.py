"""PySide6 controller UI. Device IDs are private implementation details."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QCheckBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QVBoxLayout,
    QWidget,
)

from app.core.registration import RegistrationError, load_registered_clients
from app.core.settings import Settings, load_settings, save_settings, validate_settings
from app.core.uxplay_manager import UxPlayManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPad Mirror Controller · v0.1.1")
        self.resize(680, 570)
        self.manager = UxPlayManager(self)
        try:
            self.settings = load_settings()
        except (OSError, ValueError) as exc:
            self.settings = Settings()
            QMessageBox.warning(self, "설정 확인", f"설정을 읽지 못했습니다: {exc}")
        self._make_ui()
        self.manager.status_changed.connect(self.status.setText)
        self.manager.event.connect(self._add_event)
        self.manager.pin_requested.connect(self._set_pin)
        self.manager.registration_changed.connect(self._registration_changed)
        self.manager.busy_changed.connect(self._set_running)
        self._add_event("GUI 준비 완료 — 기존 PIN 인증키와 등록 파일을 보존합니다")
        self._refresh_registration()

    def _make_ui(self):
        content = QWidget(self)
        outer = QVBoxLayout(content)
        outer.setSpacing(11)

        title = QLabel("iPad Mirror Controller")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        outer.addWidget(title)
        subtitle = QLabel("등록된 iPad 자동 연결 · 새로운 iPad는 최초 1회 PIN 등록")
        subtitle.setStyleSheet("color: #5f6670;")
        outer.addWidget(subtitle)

        status_box = QGroupBox("연결 및 인증 상태")
        status_layout = QVBoxLayout(status_box)
        self.status = QLabel("서버 중지됨")
        self.status.setStyleSheet("font-size: 17px; font-weight: 650;")
        status_layout.addWidget(self.status)
        self.device_count = QLabel("등록 정보 확인 중")
        self.device_count.setStyleSheet("color: #5f6670;")
        status_layout.addWidget(self.device_count)
        self.pin = QLabel("")
        self.pin.setStyleSheet("font-size: 20px; font-weight: 700; color: #1653a5;")
        self.pin.setWordWrap(True)
        self.pin.hide()
        status_layout.addWidget(self.pin)
        outer.addWidget(status_box)

        config_box = QGroupBox("실행 설정 (이 PC에만 저장)")
        form = QFormLayout(config_box)
        self.exe = QLineEdit(self.settings.uxplay_exe)
        self.key = QLineEdit(self.settings.key_file)
        self.registration = QLineEdit(self.settings.registration_file)
        self.receiver = QLineEdit(self.settings.receiver_name)
        self.audio = QCheckBox("서버 시작 시 소리 켜기")
        self.audio.setChecked(self.settings.audio_enabled)
        self.audio.setToolTip("실시간 음소거는 다음 개발 단계에서 추가합니다.")
        form.addRow("UxPlay 실행 파일", self.exe)
        form.addRow("PIN 인증키 파일", self.key)
        form.addRow("등록 정보 파일", self.registration)
        # No manual device ID field: this comes ONLY from registered clients.
        form.addRow("수신기 이름", self.receiver)
        form.addRow("오디오", self.audio)
        outer.addWidget(config_box)

        buttons = QHBoxLayout()
        self.start_button = QPushButton("▶ 서버 시작")
        self.start_button.setMinimumHeight(42)
        self.start_button.clicked.connect(self._start_normal)
        self.enroll_button = QPushButton("＋ 새 iPad 등록 (PIN)")
        self.enroll_button.setMinimumHeight(42)
        self.enroll_button.clicked.connect(self._start_enrollment)
        self.stop_button = QPushButton("■ 서버 중단")
        self.stop_button.setMinimumHeight(42)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.manager.stop)
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.enroll_button)
        buttons.addWidget(self.stop_button)
        outer.addLayout(buttons)

        self.mode_hint = QLabel("등록 기기는 '서버 시작'으로 연결합니다. 새 기기는 '새 iPad 등록'을 누르세요.")
        self.mode_hint.setWordWrap(True)
        self.mode_hint.setStyleSheet("color: #586274;")
        outer.addWidget(self.mode_hint)

        outer.addWidget(QLabel("동작 기록 (PIN·Device ID·IP 주소는 저장하지 않음)"))
        self.events = QPlainTextEdit()
        self.events.setReadOnly(True)
        outer.addWidget(self.events, 1)
        footnote = QLabel("iPad의 '화면 미러링'에서 수신기를 선택하세요. 서버 중단 시 이 앱이 실행한 UxPlay만 종료합니다.")
        footnote.setWordWrap(True)
        outer.addWidget(footnote)
        self.setCentralWidget(content)

    def _settings_from_ui(self) -> Settings:
        return Settings(
            uxplay_exe=self.exe.text().strip(),
            key_file=self.key.text().strip(),
            registration_file=self.registration.text().strip(),
            receiver_name=self.receiver.text().strip(),
            audio_enabled=self.audio.isChecked(),
        )

    def _refresh_registration(self):
        try:
            devices = load_registered_clients(self.registration.text().strip())
            self.device_count.setText(f"PIN 인증 완료된 기기: {len(devices)}대")
            self.device_count.setToolTip("기기 ID는 화면에 표시하지 않습니다.")
        except RegistrationError:
            self.device_count.setText("기기 등록 파일 확인 필요")

    def _registration_changed(self):
        # UxPlay logs the event immediately before appending its file.
        QTimer.singleShot(500, self._refresh_registration)
        if self.manager.pairing_mode:
            self.mode_hint.setText("등록이 완료되면 서버 중단 후 '서버 시작'으로 다시 실행하세요. 이후에는 PIN 없이 연결됩니다.")

    def _start_normal(self):
        self._launch(pairing_mode=False)

    def _start_enrollment(self):
        if self.manager.is_running():
            QMessageBox.information(self, "서버 실행 중", "먼저 서버를 중단한 후 새 iPad 등록을 시작하세요.")
            return
        result = QMessageBox.question(
            self, "새 iPad 등록",
            "신뢰할 수 있는 개인 Wi-Fi에서만 PIN 등록을 진행하세요.\n\n"
            "등록 모드에서는 같은 네트워크의 새 기기도 PIN을 요청할 수 있습니다. "
            "등록을 마치면 서버를 중단하고 일반 모드로 다시 시작하세요.\n\n"
            "PIN 등록 모드를 시작할까요?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if result == QMessageBox.StandardButton.Yes:
            self._launch(pairing_mode=True)

    def _launch(self, *, pairing_mode: bool):
        if self.manager.is_running():
            return
        settings = self._settings_from_ui()
        try:
            issues = validate_settings(settings)
            if issues:
                QMessageBox.warning(self, "설정 확인 필요", "\n".join(issues))
                return
            devices = load_registered_clients(settings.registration_file)
        except (RegistrationError, OSError) as exc:
            QMessageBox.warning(self, "등록 정보 확인 필요", str(exc))
            return
        if not pairing_mode and not devices:
            QMessageBox.information(
                self, "최초 등록 필요",
                "등록된 iPad가 없습니다. '＋ 새 iPad 등록 (PIN)' 버튼으로 최초 인증을 진행하세요.",
            )
            return
        try:
            save_settings(settings)
        except OSError as exc:
            QMessageBox.critical(self, "설정 저장 실패", str(exc))
            return
        # The device IDs are used *only* to construct hidden UxPlay arguments.
        allowed_ids = [device.device_id for device in devices]
        self.settings = settings
        self._refresh_registration()
        try:
            self.manager.start(settings, pairing_mode=pairing_mode, allowed_ids=allowed_ids)
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, "UxPlay 시작 실패", str(exc))
            return
        self._set_running(True)
        if pairing_mode:
            self.mode_hint.setText("iPad에서 화면 미러링을 선택하세요. PIN이 발급되면 위쪽에 표시됩니다.")
        else:
            self.mode_hint.setText("등록된 iPad는 PIN 없이 자동 인증됩니다. 새 기기 등록은 서버 중단 후 가능합니다.")

    def _set_running(self, running: bool):
        self.start_button.setEnabled(not running)
        self.enroll_button.setEnabled(not running)
        self.stop_button.setEnabled(running)
        for control in (self.exe, self.key, self.registration, self.receiver, self.audio):
            control.setEnabled(not running)
        if not running:
            self._refresh_registration()

    def _set_pin(self, pin: str):
        if pin:
            self.pin.setText(f"iPad에 입력할 최초 인증 PIN: {pin}")
            self.pin.show()
        else:
            self.pin.clear()
            self.pin.hide()

    def _add_event(self, message: str):
        self.events.appendPlainText(f"[{datetime.now():%H:%M:%S}] {message}")

    def closeEvent(self, event):
        if self.manager.is_running():
            self.manager.stop()
        super().closeEvent(event)
