"""
Bootstrap utilities for the MagnetarPrometheus backend runtime.

Provides dependency detection and optional auto-installation so the CLI can
report missing packages clearly and install them when policy permits.

Design rationale
----------------
The bootstrap module is intentionally kept dependency-free (only stdlib) so that
it can run before any third-party packages are confirmed to be present.  It must
be executable as the very first thing the CLI does.

Key invariants enforced by this module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Every declared dependency is *always* attempted during the installation pass,
  even if a previous one failed.  This gives the user (or operator) a complete
  picture of what is broken rather than a partial report that stops at the first
  failure ("whack-a-mole" problem described in GitHub issue #94).
- ``BootstrapResult.success`` is derived solely from whether ``failed`` is empty
  after the full loop completes, NOT from the absence of failures on the way through.
"""

import importlib
import subprocess
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class BootstrapPolicy:
    """Controls how missing dependencies are handled at startup.

    This policy object is the single place where installation behaviour is
    configured.  Keeping it separate from the result allows callers to inspect
    or override the policy without coupling it to the outcome.

    Attributes:
        auto_install: When True, missing packages are installed via pip
            automatically. When False, the caller receives a failure result
            and must handle installation itself (e.g. print a manual-install
            message and exit).
    """

    auto_install: bool = False


@dataclass
class BootstrapResult:
    """Records the outcome of a dependency-check pass.

    Every attribute is populated regardless of whether individual steps
    succeed or fail.  Callers should inspect ``failed`` to determine whether
    any remediation is still needed.

    Attributes:
        success: True when all required dependencies are available after the
            check (and optional install) completes.  False as soon as any
            dependency remains unresolvable.
        missing: Dependencies that were not importable before the check.
            Populated even when ``auto_install`` is False so callers can
            display a human-readable list.
        installed: Dependencies that were successfully installed during this
            run (subset of ``missing``).
        failed: Dependencies whose installation was attempted but failed.
            This list is *always* fully populated — the installation loop
            never short-circuits on the first failure so this list contains
            *every* dependency that could not be installed.
    """

    success: bool
    missing: List[Dict[str, str]] = field(default_factory=list)
    installed: List[Dict[str, str]] = field(default_factory=list)
    failed: List[Dict[str, str]] = field(default_factory=list)


def check_and_install_dependencies(
    dependencies: List[Dict[str, str]],
    policy: Optional[BootstrapPolicy] = None,
) -> BootstrapResult:
    """Check for all required modules and optionally install any that are missing.

    The function runs in two distinct phases:

    Phase 1 — detection
        Iterate over every entry in ``dependencies`` and try to import the
        named module.  Any entry whose import fails is added to the ``missing``
        list.  This phase always completes regardless of how many imports fail.

    Phase 2 — installation (only when ``policy.auto_install`` is True)
        Iterate over every entry in ``missing`` and invoke ``pip install`` for
        each one.  Critically, this loop **never returns early on failure**.
        Returning early on the first failure was the bug described in GitHub
        issue #94: it produced an incomplete ``failed`` list when multiple
        dependencies could not be installed, forcing the operator to fix one
        problem at a time and re-run.  By always completing the loop, the
        resulting ``BootstrapResult.failed`` list is guaranteed to contain
        *every* dependency that could not be installed in one pass.

    After phase 2 the ``success`` flag is derived from whether ``failed`` is
    empty.  This is intentional: ``success`` must reflect the final state
    (all attempted, all succeeded) rather than an optimistic default that
    happens to be True only because the loop stopped early.

    Args:
        dependencies: A list of dicts, each with at minimum the keys:
            - ``"module"``  – the Python module name used with ``importlib``
            - ``"package"`` – the pip package name used for installation
        policy: Optional policy object governing installation behaviour.
            Defaults to ``BootstrapPolicy()`` (auto_install=False) when None.

    Returns:
        A ``BootstrapResult`` where:
        - ``success`` is True only if no dependencies remain in ``failed``.
        - ``missing`` lists every dependency that was not importable up-front.
        - ``installed`` lists every dependency installed successfully this run.
        - ``failed`` lists every dependency whose installation was attempted
          but raised ``subprocess.CalledProcessError``.
    """
    # Apply a safe default so callers don't have to always supply a policy.
    if policy is None:
        policy = BootstrapPolicy()

    # --- Phase 1: detect which dependencies are absent ---
    # We never short-circuit here; every dep must be checked so that ``missing``
    # is a complete list before we even consider installation.
    missing: List[Dict[str, str]] = []
    for dep in dependencies:
        try:
            importlib.import_module(dep["module"])
        except ImportError:
            # Record and continue — do not break or return.
            missing.append(dep)

    # If nothing is missing we are done; return an unambiguous success.
    if not missing:
        return BootstrapResult(success=True)

    # Build the result object early so both early-return paths (policy=False)
    # and the installation path share the same object.
    result = BootstrapResult(success=False, missing=missing)

    # When auto-install is disabled the caller is responsible for informing the
    # user and taking corrective action; return immediately without pip calls.
    if not policy.auto_install:
        return result

    # --- Phase 2: attempt installation of every missing dependency ---
    # IMPORTANT: the except block intentionally does NOT return.  Returning on
    # the first CalledProcessError was the bug reported in issue #94.  By
    # continuing the loop we guarantee that ``result.failed`` reflects *all*
    # dependencies that pip could not install, giving operators a full picture
    # in a single run instead of requiring repeated re-runs ("whack-a-mole").
    for dep in missing:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep["package"]])
            result.installed.append(dep)
        except subprocess.CalledProcessError:
            # Record the failure and move on to the next dependency.
            # DO NOT return here — we must attempt every remaining entry.
            result.failed.append(dep)

    # Derive success from the actual outcome: only True when every installation
    # attempt succeeded (i.e. ``failed`` is empty after the full loop).
    result.success = not result.failed
    return result


def bootstrap_runtime(auto_install: bool = False) -> bool:
    """Bootstrap the runtime by checking and installing required dependencies.

    This is the high-level entry point used by the CLI at startup.  It
    declares the canonical set of packages that MagnetarPrometheus requires,
    delegates the check-and-install logic to ``check_and_install_dependencies``,
    and translates the structured ``BootstrapResult`` into human-readable
    console output before returning a simple boolean to the caller.

    Output behaviour:
    - When all dependencies are present (or were installed successfully) a
      brief confirmation is printed and True is returned.
    - When ``auto_install`` is False and dependencies are missing, the full
      list of missing packages is printed with manual-install instructions.
    - When ``auto_install`` is True but some installations failed, *every*
      failed package is reported (not just the first one — see issue #94).
    - In all failure cases False is returned so the caller can exit cleanly.

    Args:
        auto_install: When True, missing packages are installed via pip
            without user confirmation.  Defaults to False to avoid unintended
            side-effects in production environments.

    Returns:
        True  — all required dependencies are available after the check.
        False — one or more dependencies are still missing or uninstallable.
    """
    # The canonical list of runtime dependencies.  Each entry must include:
    #   "module"  — the importable Python module name (used for detection)
    #   "package" — the pip-installable package name (used for installation)
    required_deps = [
        {"module": "yaml", "package": "PyYAML"},
        {"module": "pydantic", "package": "pydantic"},
        {"module": "magnetar_prometheus_sdk", "package": "magnetar-prometheus-sdk"},
    ]

    policy = BootstrapPolicy(auto_install=auto_install)
    result = check_and_install_dependencies(required_deps, policy=policy)

    if result.success:
        if result.installed:
            print("Successfully installed missing dependencies.")
        return True

    if not policy.auto_install:
        print("Missing required dependencies:")
        for dep in result.missing:
            print(f"  - {dep['package']} (import: {dep['module']})")
        print("\nAutomatic installation is disabled or not allowed by policy.")
        print("Please install them manually using pip.")
    else:
        # Report every failed installation — not just the first one.
        # This was the user-visible symptom of the issue fixed in issue #94:
        # previously only the first failure was ever reported.
        for dep in result.failed:
            print(f"Failed to install {dep['package']}.")

    return False
