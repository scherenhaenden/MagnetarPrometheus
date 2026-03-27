import importlib
import subprocess
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class BootstrapPolicy:
    auto_install: bool = False

@dataclass
class BootstrapResult:
    success: bool
    missing: List[Dict[str, str]] = field(default_factory=list)
    installed: List[Dict[str, str]] = field(default_factory=list)
    failed: List[Dict[str, str]] = field(default_factory=list)

def check_and_install_dependencies(dependencies: List[Dict[str, str]], policy: Optional[BootstrapPolicy] = None) -> BootstrapResult:
    if policy is None:
        policy = BootstrapPolicy()

    missing = []
    for dep in dependencies:
        try:
            importlib.import_module(dep["module"])
        except ImportError:
            missing.append(dep)

    if not missing:
        return BootstrapResult(success=True)

    result = BootstrapResult(success=False, missing=missing)

    if not policy.auto_install:
        return result

    for dep in missing:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep["package"]])
            result.installed.append(dep)
        except subprocess.CalledProcessError:
            result.failed.append(dep)
            return result

    result.success = True
    return result

def bootstrap_runtime(auto_install: bool = False) -> bool:
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
        for dep in result.failed:
            print(f"Failed to install {dep['package']}.")

    return False
