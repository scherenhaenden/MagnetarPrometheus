import datetime
import re
from pathlib import Path
from typing import Optional

VERSION_STAMP_PATTERN = re.compile(r"^\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$")


def _generate_canonical_version_stamp() -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.strftime("%Y.%m.%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}"


def _candidate_release_version_paths(override_path: Optional[str] = None) -> list[Path]:
    """def _candidate_release_version_paths(override_path: Optional[str] = None) ->
    list[Path]:
    Generate candidate release version paths.  This function constructs a list of
    potential release version file paths.  If an `override_path` is provided, it is
    added to the list of candidates.  The function also traverses the parent
    directories of the current module's  path to include "release-version.txt"
    files. Duplicate paths are resolved  and filtered out to ensure uniqueness
    before returning the final list.
    
    Args:
        override_path (Optional[str]): An optional path to override the default"""
    candidates: list[Path] = []

    if override_path:
        candidates.append(Path(override_path))

    module_path = Path(__file__).resolve()
    for parent in module_path.parents:
        candidates.append(parent / "release-version.txt")

    unique_candidates: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve(strict=False)
        if resolved not in seen:
            unique_candidates.append(candidate)
            seen.add(resolved)

    return unique_candidates


def get_canonical_version_stamp(override_path: Optional[str] = None) -> str:
    """Returns the canonical version stamp for MagnetarPrometheus.
    
    The function attempts to retrieve the version stamp from a  `release-
    version.txt` file by searching upward from the current  module toward the
    repository root. If the file is not found,  unreadable, empty, or does not
    match the expected format, it  generates the current UTC timestamp as a
    fallback. The version  stamp follows the format: yyyy.MM.dd HH:mm:ss.SSS.
    """
    for path in _candidate_release_version_paths(override_path):
        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue

        if content and VERSION_STAMP_PATTERN.fullmatch(content):
            return content

    return _generate_canonical_version_stamp()
