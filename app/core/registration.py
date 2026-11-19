"""Read the local UxPlay PIN register without exposing device identifiers in UI.

UxPlay 1.73.7 stores:
    base64_public_key,device_id,device_name

UxPlay 1.74+ may store:
    base64_public_key,timestamp,device_id,device_name

Its C++ reader trusts the first 44 bytes as a base64 public key.  We
intentionally fail closed on unrecognized active entries rather than silently
starting in unrestricted mode or using data that might not be valid.
"""

from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass
from pathlib import Path

_DEVICE_ID_RE = re.compile(r"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\Z")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\Z")


class RegistrationError(ValueError):
    """The register is unreadable or contains unexpected active entries."""


@dataclass(frozen=True)
class RegisteredClient:
    device_id: str
    name: str


def load_registered_clients(filename: str) -> list[RegisteredClient]:
    """Return verified local device IDs, never key material or log content.

    A missing register means no client has been paired on this computer yet.
    """
    if not filename.strip():
        raise RegistrationError("등록 파일 경로가 비어 있습니다.")
    path = Path(filename)
    if not path.exists():
        return []
    if not path.is_file():
        raise RegistrationError("등록 경로가 파일이 아닙니다.")
    try:
        content = path.read_text(encoding="utf-8-sig")
    except (UnicodeError, OSError) as exc:
        raise RegistrationError("등록 파일을 읽을 수 없습니다.") from exc

    clients: dict[str, RegisteredClient] = {}
    for number, raw in enumerate(content.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(",", 3)
        if len(fields) == 3:  # UxPlay 1.73.7: PK,DeviceID,Name
            public_key, device_id, device_name = fields
            timestamp = None
        elif len(fields) == 4:  # Newer UxPlay: PK,Timestamp,DeviceID,Name
            public_key, timestamp, device_id, device_name = fields
        else:
            raise RegistrationError(f"등록 파일 {number}행 형식을 인식할 수 없습니다.")
        try:
            key_bytes = base64.b64decode(public_key.strip(), validate=True)
        except (ValueError, binascii.Error) as exc:
            raise RegistrationError(f"등록 파일 {number}행의 키 형식이 올바르지 않습니다.") from exc
        timestamp_ok = timestamp is None or bool(_DATE_RE.fullmatch(timestamp.strip()))
        if len(key_bytes) != 32 or not timestamp_ok or not _DEVICE_ID_RE.fullmatch(device_id.strip()):
            raise RegistrationError(f"등록 파일 {number}행의 구조가 올바르지 않습니다.")
        normalized_id = device_id.strip().upper()
        clients[normalized_id] = RegisteredClient(device_id=normalized_id, name=device_name.strip())
    return list(clients.values())
