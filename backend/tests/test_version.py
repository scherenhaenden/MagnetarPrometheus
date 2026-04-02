import os
import pytest
import datetime
from unittest.mock import patch, mock_open

from magnetar_prometheus.version import get_canonical_version_stamp

def test_get_canonical_version_stamp_from_file(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("2026.03.26 12:00:00.123")

    version = get_canonical_version_stamp(override_path=str(version_file))
    assert version == "2026.03.26 12:00:00.123"

def test_get_canonical_version_stamp_empty_file(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("   \n") # empty/whitespace

    # with an empty file it should fallback to dynamic timestamp
    # we just check the format of the output
    version = get_canonical_version_stamp(override_path=str(version_file))
    assert len(version) >= 23 # yyyy.MM.dd HH:mm:ss.SSS is 23 chars
    assert "." in version
    assert ":" in version

def test_get_canonical_version_stamp_file_read_error(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("2026.03.26 12:00:00.123")

    # Mock open to raise an OSError when reading the file
    with patch("builtins.open", side_effect=OSError("Permission denied")):
        version = get_canonical_version_stamp(override_path=str(version_file))
        assert len(version) >= 22

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
