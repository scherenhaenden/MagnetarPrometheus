import datetime
from pathlib import Path
from unittest.mock import patch

from magnetar_prometheus.version import (
    _candidate_release_version_paths,
    get_canonical_version_stamp,
)

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
    assert len(version) == 23  # yyyy.MM.dd HH:mm:ss.SSS
    assert version.count(".") == 3
    assert version.count(":") == 2

def test_get_canonical_version_stamp_file_read_error(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("2026.03.26 12:00:00.123")

    # Mock open to raise an OSError when reading the file
    with patch("pathlib.Path.read_text", side_effect=OSError("Permission denied")):
        version = get_canonical_version_stamp(override_path=str(version_file))
        assert len(version) == 23

def test_get_canonical_version_stamp_invalid_file_falls_back(tmp_path):
    version_file = tmp_path / "release-version.txt"
    version_file.write_text("not-a-version-stamp")

    version = get_canonical_version_stamp(override_path=str(version_file))
    assert version != "not-a-version-stamp"
    assert len(version) == 23

def test_get_canonical_version_stamp_dynamic_fallback():
    # Make sure we don't accidentally read a real file in the repo
    with patch("magnetar_prometheus.version._candidate_release_version_paths", return_value=[]):
        # We mock datetime to ensure consistent generation
        fixed_dt = datetime.datetime(2026, 3, 26, 12, 5, 10, 45000, tzinfo=datetime.timezone.utc)
        class MockDateTime:
            @classmethod
            def now(cls, tz=None):
                return fixed_dt

        with patch("magnetar_prometheus.version.datetime.datetime", MockDateTime):
            version = get_canonical_version_stamp()
            assert version == "2026.03.26 12:05:10.045"

def test_candidate_release_version_paths_searches_upward(tmp_path):
    module_file = tmp_path / "backend" / "src" / "magnetar_prometheus" / "version.py"
    module_file.parent.mkdir(parents=True)
    module_file.write_text("# test module")

    with patch("magnetar_prometheus.version.__file__", str(module_file)):
        candidates = _candidate_release_version_paths()

    assert module_file.parent / "release-version.txt" in candidates
    assert (tmp_path / "release-version.txt") in candidates
