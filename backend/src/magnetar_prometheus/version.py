"""
Version helpers for the MagnetarPrometheus backend.

Why this file exists in this form:

- The repository uses a timestamp-oriented version convention rather than a manually bumped
  semantic version for the current proof-of-concept slice. That means the backend needs one
  small, deterministic place that can answer the question "what version stamp should this
  build/report/release expose right now?"
- The helper must work in both CI/release contexts and ordinary local development contexts.
  In release flows, a precomputed `release-version.txt` artifact may already exist and should
  win. In ad hoc local execution, that artifact may not exist yet, so the helper must fall
  back to a generated UTC timestamp without failing.
- The search behavior is intentionally simple and file-system based because the project is
  still lightweight. The code checks a small set of conventional relative paths rather than
  requiring a heavier packaging or runtime-configuration layer before the application has
  actually earned that complexity.
- This module stays narrow on purpose: it does not attempt to own release policy, CI setup,
  or artifact generation. Its responsibility is only to resolve the canonical version stamp
  from the sources that the rest of the repository already treats as authoritative.
"""

import datetime
import os
from typing import Optional


def get_canonical_version_stamp(override_path: Optional[str] = None) -> str:
    """Return the canonical MagnetarPrometheus version stamp.

    The repository's canonical format is ``yyyy.MM.dd HH:mm:ss.SSS``. The helper resolves
    that stamp in a precedence order that matches how the repository is operated:

    1. If an explicit ``override_path`` is supplied, check that location first. This is used
       by tests or controlled tooling that wants to point directly at a known artifact.
    2. Otherwise, check the conventional relative ``release-version.txt`` locations that may
       exist depending on whether the backend is being run from the package directory, the
       repository root, or a nearby automation context.
    3. If no readable artifact exists, synthesize a UTC timestamp in the canonical format so
       the caller still receives a stable, non-empty version string.

    This fallback behavior is deliberate: local development and bootstrap paths should remain
    runnable even before a formal release artifact has been generated.
    """
    # These are the conventional artifact locations this backend may run under. They are kept
    # in explicit order because the first readable non-empty file should be treated as the
    # authoritative release stamp for the current invocation context.
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
                # A blank artifact should not silently become the canonical version. Only a
                # non-empty file is considered authoritative; otherwise we continue searching
                # so a valid artifact in a nearby conventional location can still win.
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return content
            except OSError:
                # Read failures should not break callers that merely want a usable version
                # stamp. If one candidate path is unreadable, continue checking the remaining
                # conventional locations before finally falling back to a generated timestamp.
                continue

    # When no artifact is available, the backend still needs a deterministic release-style
    # identifier for logs, diagnostics, and local execution output, so we synthesize one from
    # the current UTC time using the repository's canonical timestamp shape.
    now = datetime.datetime.now(datetime.timezone.utc)
    ms = f"{now.microsecond // 1000:03d}"
    return now.strftime(f"%Y.%m.%d %H:%M:%S{ms}")
