# actions/open_app.py
# MARK XXXV — macOS App Launcher

import time
import subprocess
import shutil

try:
    import psutil
    _PSUTIL = True
except ImportError:
    _PSUTIL = False

_APP_ALIASES = {
    "whatsapp":           "WhatsApp",
    "chrome":             "Google Chrome",
    "google chrome":      "Google Chrome",
    "firefox":            "Firefox",
    "spotify":            "Spotify",
    "vscode":             "Visual Studio Code",
    "visual studio code": "Visual Studio Code",
    "discord":            "Discord",
    "telegram":           "Telegram",
    "instagram":          "Instagram",
    "tiktok":             "TikTok",
    "notepad":            "TextEdit",
    "textedit":           "TextEdit",
    "calculator":         "Calculator",
    "terminal":           "Terminal",
    "iterm":              "iTerm",
    "explorer":           "Finder",
    "finder":             "Finder",
    "file explorer":      "Finder",
    "preview":            "Preview",
    "paint":              "Preview",
    "word":               "Microsoft Word",
    "excel":              "Microsoft Excel",
    "powerpoint":         "Microsoft PowerPoint",
    "vlc":                "VLC",
    "zoom":               "zoom.us",
    "slack":              "Slack",
    "steam":              "Steam",
    "activity monitor":   "Activity Monitor",
    "task manager":       "Activity Monitor",
    "settings":           "System Settings",
    "system preferences": "System Settings",
    "system settings":    "System Settings",
    "edge":               "Microsoft Edge",
    "brave":              "Brave Browser",
    "obsidian":           "Obsidian",
    "notion":             "Notion",
    "blender":            "Blender",
    "capcut":             "CapCut",
    "postman":            "Postman",
    "figma":              "Figma",
    "messages":           "Messages",
    "imessage":           "Messages",
    "mail":               "Mail",
    "safari":             "Safari",
    "music":              "Music",
    "photos":             "Photos",
    "keynote":            "Keynote",
    "pages":              "Pages",
    "numbers":            "Numbers",
    "xcode":              "Xcode",
    "cursor":             "Cursor",
}


def _normalize(raw: str) -> str:
    key = raw.lower().strip()
    if key in _APP_ALIASES:
        return _APP_ALIASES[key]
    for alias_key, app_name in _APP_ALIASES.items():
        if alias_key in key or key in alias_key:
            return app_name
    return raw


def _is_running(app_name: str) -> bool:
    if not _PSUTIL:
        return True
    app_lower = app_name.lower().replace(" ", "")
    try:
        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = proc.info["name"].lower().replace(" ", "")
                if app_lower in proc_name or proc_name in app_lower:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    return False


def _launch(app_name: str) -> bool:
    # Try open -a first
    try:
        result = subprocess.run(["open", "-a", app_name], capture_output=True, timeout=8)
        if result.returncode == 0:
            time.sleep(1.0)
            return True
    except Exception:
        pass

    # Try with .app suffix
    try:
        result = subprocess.run(["open", "-a", f"{app_name}.app"], capture_output=True, timeout=8)
        if result.returncode == 0:
            time.sleep(1.0)
            return True
    except Exception:
        pass

    # Fallback: Spotlight
    try:
        import pyautogui
        pyautogui.hotkey("command", "space")
        time.sleep(0.6)
        pyautogui.write(app_name, interval=0.05)
        time.sleep(0.8)
        pyautogui.press("enter")
        time.sleep(1.5)
        return True
    except Exception as e:
        print(f"[open_app] Spotlight failed: {e}")
        return False


def open_app(
    parameters=None,
    response=None,
    player=None,
    session_memory=None,
) -> str:
    app_name = (parameters or {}).get("app_name", "").strip()

    if not app_name:
        return "Please specify which application to open, sir."

    normalized = _normalize(app_name)
    print(f"[open_app] Launching: {app_name} -> {normalized}")

    if player:
        player.write_log(f"[open_app] {app_name}")

    try:
        success = _launch(normalized)

        if success:
            return f"Opened {app_name} successfully, sir."

        if normalized != app_name:
            success = _launch(app_name)
            if success:
                return f"Opened {app_name} successfully, sir."

        return (
            f"I tried to open {app_name}, sir, but couldn't confirm it launched. "
            f"It may still be loading or might not be installed."
        )

    except Exception as e:
        print(f"[open_app] Error: {e}")
        return f"Failed to open {app_name}, sir: {e}"
