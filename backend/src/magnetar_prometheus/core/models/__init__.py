"""Re-export shim for core domain models.

Runtime model types live in ``magnetar_prometheus_sdk``; this package exists
to provide a stable internal import path for backend code that needs to
reference them without coupling directly to the SDK package name.
"""
