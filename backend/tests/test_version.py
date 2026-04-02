import datetime
import re
from unittest.mock import patch

from magnetar_prometheus.version import get_canonical_version_stamp

def test_get_canonical_version_stamp_from_file(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("2026.03.26 12:00:00.123")

    version = get_canonical_version_stamp(override_path=str(version_file))
    assert version == "2026.03.26 12:00:00.123"

def test_get_canonical_version_stamp_empty_file(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("   \n")  # empty/whitespace

    # With an empty file the helper should fall back to a generated timestamp
    # and that timestamp should match the full canonical format, not merely a
    # loose "contains a dot and colon somewhere" approximation.
    version = get_canonical_version_stamp(override_path=str(version_file))
    assert re.match(
        r"^\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$",
        version,
    ), f"Version '{version}' does not match canonical format"

def test_get_canonical_version_stamp_file_read_error(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("2026.03.26 12:00:00.123")

    # A read failure should trigger the same generated canonical fallback shape
    # as any other missing/unusable artifact path.
    with patch("builtins.open", side_effect=OSError("Permission denied")):
        version = get_canonical_version_stamp(override_path=str(version_file))
        assert re.match(
            r"^\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$",
            version,
        ), f"Version '{version}' does not match canonical format"

def test_get_canonical_version_stamp_dynamic_fallback():
    # Make sure we don't accidentally read a real file in the repo
    with patch("os.path.exists", return_value=False):
        # We mock datetime to ensure consistent generation
        fixed_dt = datetime.datetime(2026, 3, 26, 12, 5, 10, 45000, tzinfo=datetime.timezone.utc)
        class MockDateTime:
            @classmethod
            def now(cls, tz=None):
                return fixed_dt

        with patch("magnetar_prometheus.version.datetime.datetime", MockDateTime):
            version = get_canonical_version_stamp()
            assert version == "2026.03.26 12:05:10.045"
