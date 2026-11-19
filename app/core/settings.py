"""Local configuration. No PIN, private key or device ID is embedded in source."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL_SETTINGS = ROOT / "settings.local.json"


@dataclass
class Settings:
    uxplay_exe: str = ""
    key_file: str = ""
    registration_file: str = ""
    receiver_name: str = "UxPlay-NewPair"
    audio_enabled: bool = True


def _discover() -> Settings:
    settings = Settings()
    home_root = Path("C:/msys64/home")
    if not home_root.is_dir():
        return settings
    for home in sorted(home_root.iterdir()):
        exe = home / "projects/UxPlay/build/uxplay.exe"
        if exe.is_file():
            settings.uxplay_exe = str(exe)
            settings.key_file = str(home / ".uxplay-pin-test.pem")
            settings.registration_file = str(home / ".uxplay-pin-test.register")
            break
    return settings


def load_settings() -> Settings:
    settings = _discover()
    if not LOCAL_SETTINGS.is_file():
        return settings
    data = json.loads(LOCAL_SETTINGS.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("설정 파일은 JSON 객체여야 합니다.")
    for key in asdict(settings):
        if key in data and type(data[key]) is type(getattr(settings, key)):
            setattr(settings, key, data[key])
    # v0.1.0's obsolete device_id field is deliberately ignored and removed
    # the next time the settings are saved.
    return settings


def save_settings(settings: Settings) -> None:
    LOCAL_SETTINGS.write_text(
        json.dumps(asdict(settings), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def validate_settings(settings: Settings) -> list[str]:
    issues = []
    if not settings.uxplay_exe or not Path(settings.uxplay_exe).is_file():
        issues.append("UxPlay 실행 파일을 찾을 수 없습니다.")
    if not settings.key_file.strip():
        issues.append("인증키 파일 경로가 비어 있습니다.")
    if not settings.registration_file.strip():
        issues.append("등록 파일 경로가 비어 있습니다.")
    if not settings.receiver_name.strip():
        issues.append("수신기 이름을 입력하세요.")
    # For a first pairing, UxPlay creates a new key and registration file.
    # However, a lost key with an existing registration is not silently reset.
    if settings.key_file and settings.registration_file:
        key = Path(settings.key_file)
        register = Path(settings.registration_file)
        if register.is_file() and register.stat().st_size > 0 and not key.is_file():
            issues.append("등록 파일은 있으나 기존 인증키가 없습니다. 기존 키를 복구하세요.")
        if key.exists() and not key.is_file():
            issues.append("인증키 경로가 파일이 아닙니다.")
    return issues
