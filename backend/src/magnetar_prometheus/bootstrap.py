"""
Bootstrap utilities for the MagnetarPrometheus backend runtime.

This module exists so the CLI can verify required third-party dependencies
*before* the rest of the runtime assumes those packages are importable.
That startup position is why the module is deliberately limited to standard
library imports only: bootstrap code must remain runnable even when the very
dependencies it is checking are absent.

Why this module is intentionally explicit
----------------------------------------
The repository treats bootstrap as operator-facing runtime policy, not as a
throwaway helper. The code here therefore carries unusually heavy explanation
on purpose. The comments are meant to tell future agents and maintainers:

- what each bootstrap stage does
- why dependency detection and installation are split into two passes
- why installation attempts must continue after individual failures
- why the result object is structured instead of being inferred from prints
- which behavioural guarantees should remain stable unless a clearly better
  replacement is implemented end-to-end

The most important invariant preserved here is that installation attempts must
never stop on the first failing package. The user needs a complete report of
every unresolved dependency in one run; otherwise the CLI degrades into a
repeated fix-one-rerun-one loop that hides the full problem set.
"""

import importlib
import subprocess
import sys
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class DependencySpec:
    """Describe one runtime dependency using both its import and install names.

    The bootstrap code needs two identifiers for every dependency because the
    Python import name and the pip package name are not always identical. A
    dedicated dataclass makes that contract visible in one place instead of
    scattering fragile ``dep["module"]`` and ``dep["package"]`` lookups
    through the file and its tests.

    Attributes:
        module: Import name used during detection with ``importlib``.
        package: Package name passed to ``pip install`` during remediation.
    """

    module: str
    package: str

    def __post_init__(self) -> None:
        """Validate the dependency shape early so bootstrap contracts stay explicit.

        This validation is not about shell escaping. The subprocess call below
        already uses ``check_call([...])`` with argument-vector form and never
        enables ``shell=True``, so shell metacharacters are not interpreted by a
        shell. The point here is different: bootstrap should reject obviously
        malformed dependency specs early instead of quietly carrying empty or
        whitespace-padded identifiers deeper into runtime startup logic.

        Keeping this validation on the dataclass also makes the contract easier
        for future agents to understand. A dependency spec is supposed to be a
        deliberate runtime declaration, not a loosely shaped dict that accepts
        arbitrary missing/blank values by accident.
        """

        if not self.module or not self.module.strip():
            raise ValueError("DependencySpec.module must be a non-empty string.")
        if not self.package or not self.package.strip():
            raise ValueError("DependencySpec.package must be a non-empty string.")
        if self.module != self.module.strip():
            raise ValueError("DependencySpec.module must not contain outer whitespace.")
        if self.package != self.package.strip():
            raise ValueError("DependencySpec.package must not contain outer whitespace.")


@dataclass
class BootstrapPolicy:
    """Controls how missing dependencies are handled at startup.

    This policy object separates operator intent from the bootstrap result.
    Keeping policy distinct from output matters because callers may want to
    inspect, override, or log startup policy without conflating it with whether
    dependency installation actually succeeded.

    Attributes:
        auto_install: When True, missing packages are installed via pip
            automatically. When False, bootstrap reports the missing packages
            and returns control to the caller without invoking pip.
    """

    auto_install: bool = False


@dataclass
class BootstrapResult:
    """Record the complete outcome of one dependency-check pass.

    The result object is intentionally structured because bootstrap has to
    serve both machine-readable decisions and human-readable CLI reporting.
    The caller must be able to distinguish:

    - which dependencies were missing up front
    - which missing dependencies were installed successfully
    - which installation attempts still failed

    The ``success`` field is therefore derived from the final state after the
    full installation pass completes, not from an optimistic assumption made
    before every missing dependency has been attempted.

    Attributes:
        success: True only when no dependencies remain unresolved after the
            check and optional install pass finish.
        missing: Every dependency that was not importable during detection.
        installed: Missing dependencies that were installed successfully.
        failed: Missing dependencies whose installation attempt still failed.
    """

    success: bool
    missing: List[DependencySpec] = field(default_factory=list)
    installed: List[DependencySpec] = field(default_factory=list)
    failed: List[DependencySpec] = field(default_factory=list)


def check_and_install_dependencies(
    dependencies: List[DependencySpec],
    policy: Optional[BootstrapPolicy] = None,
) -> BootstrapResult:
    """Check required modules and optionally install every missing dependency.

    The workflow is deliberately split into two full passes.

    Detection pass:
        Iterate over *all* dependency specs and attempt their imports. Missing
        entries are accumulated into ``missing`` rather than triggering any
        immediate install work. This guarantees the caller can inspect a full
        picture of the unresolved environment before installation policy is
        applied.

    Installation pass:
        When ``policy.auto_install`` is enabled, iterate over every dependency
        in ``missing`` and invoke pip for each one. This loop must never return
        early after a single ``CalledProcessError``. That behaviour is the
        exact regression this branch fixes: early return hid later failures and
        prevented ``BootstrapResult.failed`` from representing the full problem
        set. The correct contract is "attempt them all, report them all."

    Args:
        dependencies: Dependency specifications containing both import names
            and install names.
        policy: Optional installation policy. When omitted, bootstrap uses the
            safe default policy with ``auto_install=False``.

    Returns:
        A fully-populated ``BootstrapResult`` describing the final bootstrap
        outcome after every relevant detection and installation attempt.
    """
    if policy is None:
        policy = BootstrapPolicy()

    # Detection must inspect every dependency before the function decides what
    # to do next. The list must be complete whether installation is enabled or
    # not, because both CLI reporting and automated tests rely on that full
    # missing set being visible.
    missing: List[DependencySpec] = []
    for dep in dependencies:
        try:
            importlib.import_module(dep.module)
        except ImportError:
            missing.append(dep)

    if not missing:
        return BootstrapResult(success=True)

    result = BootstrapResult(success=False, missing=missing)

    if not policy.auto_install:
        return result

    # Installation attempts intentionally continue after failures. The user
    # needs one complete unresolved-dependency report, not a sequence of
    # partial reports that reveal only the first broken package per run.
    for dep in missing:
        try:
            # Security/audit note:
            # This subprocess invocation intentionally uses argv-list form and
            # does not enable ``shell=True``. That means the package string is
            # passed to the pip process as one argument, not interpolated by a
            # shell. ``DependencySpec`` validation above further constrains the
            # bootstrap declaration shape so obviously malformed values fail
            # early instead of silently entering runtime startup.
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep.package])
            result.installed.append(dep)
        except subprocess.CalledProcessError:
            result.failed.append(dep)

    # Success is derived from the final unresolved set after the loop ends.
    result.success = not result.failed
    return result


def bootstrap_runtime(auto_install: bool = False) -> bool:
    """Bootstrap the runtime and print the user-facing dependency outcome.

    This function is the CLI-facing orchestration layer over the lower-level
    dependency checker. It declares the canonical runtime dependency list,
    applies the requested installation policy, and turns the structured result
    into console output that explains what the operator should do next.

    The output contract should stay stable unless a clearly better replacement
    updates both callers and tests together:

    - success with no installs: return True quietly
    - success with installs: print a confirmation and return True
    - failure with auto-install disabled: print every missing package and
      instruct the operator to install them manually
    - failure with auto-install enabled: print every failed installation so the
      unresolved dependency set is visible in one pass

    Args:
        auto_install: Whether bootstrap may invoke pip automatically for
            missing runtime dependencies.

    Returns:
        True when runtime dependencies are available after bootstrap completes;
        otherwise False.
    """
    required_deps = [
        DependencySpec(module="yaml", package="PyYAML"),
        DependencySpec(module="pydantic", package="pydantic"),
        DependencySpec(module="magnetar_prometheus_sdk", package="magnetar-prometheus-sdk"),
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
            print(f"  - {dep.package} (import: {dep.module})")
        print("\nAutomatic installation is disabled or not allowed by policy.")
        print("Please install them manually using pip.")
    else:
        # Every failed dependency is reported individually so the CLI surface
        # matches the non-short-circuiting installation contract above.
        for dep in result.failed:
            print(f"Failed to install {dep.package}.")

    return False
