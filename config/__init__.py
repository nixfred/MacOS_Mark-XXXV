# config/__init__.py
import json
import platform
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent / "api_keys.json"


def get_config() -> dict:
    if not _CONFIG_PATH.exists():
        return {}
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_os() -> str:
    """Returns: 'windows' | 'mac' | 'linux'"""
    override = get_config().get("os_system")
    if override:
        return override.lower()
    sysname = platform.system().lower()
    if sysname == "darwin":
        return "mac"
    if sysname == "windows":
        return "windows"
    return "linux"


def is_windows() -> bool: return get_os() == "windows"
def is_mac() -> bool: return get_os() == "mac"
def is_linux() -> bool: return get_os() == "linux"
