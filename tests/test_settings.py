import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.command import build_uxplay_args
from app.core.registration import RegistrationError, load_registered_clients
from app.core.settings import Settings

# Synthetic, deterministic 32-byte value: not from a real paired device.
KEY = "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8="
DUMMY_ID = "AA:BB:CC:DD:EE:FF"


class RegistrationTests(unittest.TestCase):
    def test_missing_register_is_not_paired(self):
        with TemporaryDirectory() as folder:
            self.assertEqual([], load_registered_clients(str(Path(folder) / "missing.register")))

    def test_reads_uxplay_three_field_format_1737(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "test.register"
            path.write_text(f"{KEY},{DUMMY_ID},Test iPad\n", encoding="utf-8")
            clients = load_registered_clients(str(path))
            self.assertEqual([DUMMY_ID], [client.device_id for client in clients])
            self.assertEqual("Test iPad", clients[0].name)

    def test_reads_newer_four_field_format(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "test.register"
            path.write_text(f"{KEY},2026-11-19 12:34:56,{DUMMY_ID},Test iPad\n", encoding="utf-8")
            clients = load_registered_clients(str(path))
            self.assertEqual([DUMMY_ID], [client.device_id for client in clients])
            self.assertEqual("Test iPad", clients[0].name)

    def test_malformed_active_row_fails_closed(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "test.register"
            path.write_text("not-a-valid-record\n", encoding="utf-8")
            with self.assertRaises(RegistrationError):
                load_registered_clients(str(path))

    def test_comments_and_duplicates(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "test.register"
            line = f"{KEY},2026-11-19 12:34:56,{DUMMY_ID},iPad\n"
            path.write_text("# registered clients\n" + line + line, encoding="utf-8")
            self.assertEqual(1, len(load_registered_clients(str(path))))


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(
            uxplay_exe="uxplay.exe", key_file="my-key.pem", registration_file="devices.register"
        )

    def test_normal_mode_restricts_to_registered_devices(self):
        args = build_uxplay_args(self.settings, pairing_mode=False, allowed_ids=[DUMMY_ID])
        self.assertIn("-restrict", args)
        self.assertIn("-allow", args)
        self.assertIn(DUMMY_ID, args)
        self.assertIn("-pin", args)
        self.assertIn("-reg", args)
        self.assertNotIn("-vsync", args)

    def test_no_normal_mode_without_registration(self):
        with self.assertRaises(ValueError):
            build_uxplay_args(self.settings, pairing_mode=False, allowed_ids=[])

    def test_pairing_mode_requires_pin_without_allowlist(self):
        args = build_uxplay_args(self.settings, pairing_mode=True, allowed_ids=[], pairing_pin="1234")
        self.assertIn("-pin", args)
        self.assertIn("-reg", args)
        self.assertNotIn("-restrict", args)
        self.assertNotIn("-allow", args)
        self.assertEqual(args[args.index("-pin") + 1], "1234")

    def test_audio_disable_only_if_requested(self):
        self.assertNotIn("-as", build_uxplay_args(self.settings, pairing_mode=True, allowed_ids=[], pairing_pin="1234"))
        self.settings.audio_enabled = False
        args = build_uxplay_args(self.settings, pairing_mode=True, allowed_ids=[], pairing_pin="1234")
        self.assertEqual(args[-2:], ["-as", "0"])

    def test_pairing_mode_requires_valid_four_digit_pin(self):
        for bad_pin in (None, "", "12", "abcdef", "10000"):
            with self.subTest(pin=bad_pin):
                with self.assertRaises(ValueError):
                    build_uxplay_args(self.settings, pairing_mode=True, allowed_ids=[], pairing_pin=bad_pin)

    def test_settings_contain_no_device_id(self):
        self.assertNotIn("device_id", Settings.__dataclass_fields__)


if __name__ == "__main__":
    unittest.main()
