import datetime
import re
from pathlib import Path
from typing import Optional

VERSION_STAMP_PATTERN = re.compile(r"^\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$")


def _generate_canonical_version_stamp() -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.strftime("%Y.%m.%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}"


def _candidate_release_version_paths(override_path: Optional[str] = None) -> list[Path]:
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
    """
    Returns the canonical version stamp for MagnetarPrometheus.

    The format follows the rule: yyyy.MM.dd HH:mm:ss.SSS

    It first attempts to read this from a canonical `release-version.txt` file,
    located deterministically by searching upward from this module toward the
    repository root. If the file is missing, unreadable, empty, or malformed, it
    falls back to generating the current UTC timestamp dynamically.
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
