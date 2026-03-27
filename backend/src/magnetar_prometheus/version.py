import os
import datetime
from typing import Optional

def get_canonical_version_stamp(override_path: Optional[str] = None) -> str:
    """
    Returns the canonical version stamp for MagnetarPrometheus.

    The format follows the rule: yyyy.MM.dd HH:mm:sss

    It first attempts to read this from a 'release-version.txt' file
    (which may be dropped by the CI/release pipeline at the repo root or current directory).
    If the file does not exist, it falls back to generating the current UTC timestamp
    dynamically.
    """
    paths_to_check = [
        "release-version.txt",
        "../release-version.txt",
        "../../release-version.txt",
    ]

    if override_path:
        paths_to_check.insert(0, override_path)

    for path in paths_to_check:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return content
            except OSError:
                continue

    # Fallback to current UTC time
    now = datetime.datetime.now(datetime.timezone.utc)
    # Ensure zero-padding for milliseconds
    ms = f"{now.microsecond // 1000:03d}"
    return now.strftime(f"%Y.%m.%d %H:%M:%S{ms}")
