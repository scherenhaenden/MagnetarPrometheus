import importlib
import subprocess
import sys

def check_and_install_dependencies(dependencies, auto_install=False):
    missing = []
    for dep in dependencies:
        try:
            importlib.import_module(dep["module"])
        except ImportError:
            missing.append(dep)

    if not missing:
        return True

    if not auto_install:
        print("Missing required dependencies:")
        for dep in missing:
            print(f"  - {dep['package']} (import: {dep['module']})")
        print("\nAutomatic installation is disabled or not allowed by policy.")
        print("Please install them manually using pip.")
        return False

    print("Attempting automatic installation of missing dependencies...")
    for dep in missing:
        print(f"Installing {dep['package']}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep["package"]])
            print(f"Successfully installed {dep['package']}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {dep['package']}.")
            return False

    return True

def bootstrap_runtime(auto_install=False):
    required_deps = [
        {"module": "yaml", "package": "PyYAML"},
        {"module": "pydantic", "package": "pydantic"},
        {"module": "magnetar_prometheus_sdk", "package": "magnetar-prometheus-sdk"},
    ]
    return check_and_install_dependencies(required_deps, auto_install=auto_install)
