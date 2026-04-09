# actions/computer_settings.py
# MARK XXXV — macOS Computer Settings & UI Controls
#
# Intent detection via Gemini (multi-language)
# macOS-native: osascript, pmset, networksetup, pyautogui

import time
import subprocess
import sys
from pathlib import Path

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE    = 0.05
    _PYAUTOGUI = True
except ImportError:
    _PYAUTOGUI = False

try:
    import pyperclip
    _PYPERCLIP = True
except ImportError:
    _PYPERCLIP = False

import json


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR        = get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


# ── Volume ────────────────────────────────────────────────────────────────────

def volume_up():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])

def volume_down():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])

def volume_mute():
    subprocess.run(["osascript", "-e", "set volume with output muted"])

def volume_set(value: int):
    value = max(0, min(100, value))
    subprocess.run(["osascript", "-e", f"set volume output volume {value}"])
    print(f"[Settings] Volume -> {value}%")


# ── Brightness ────────────────────────────────────────────────────────────────

def brightness_up():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 144'])

def brightness_down():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 145'])


# ── Window Management ────────────────────────────────────────────────────────

def close_app():
    pyautogui.hotkey("command", "q")

def close_window():
    pyautogui.hotkey("command", "w")

def full_screen():
    pyautogui.hotkey("ctrl", "command", "f")

def minimize_window():
    pyautogui.hotkey("command", "m")

def maximize_window():
    subprocess.run(["osascript", "-e",
        'tell application "System Events" to keystroke "f" using {control down, command down}'])

def snap_left():
    # macOS Sequoia+ has native tiling; older versions need Rectangle/Magnet
    pyautogui.hotkey("ctrl", "option", "left")

def snap_right():
    pyautogui.hotkey("ctrl", "option", "right")

def switch_window():
    pyautogui.hotkey("command", "tab")

def show_desktop():
    pyautogui.hotkey("fn", "f11")

def open_task_manager():
    subprocess.Popen(["open", "-a", "Activity Monitor"])

def open_task_view():
    # Mission Control
    subprocess.run(["osascript", "-e",
        'tell application "Mission Control" to launch'])


# ── Browser / Navigation ─────────────────────────────────────────────────────

def focus_search():
    pyautogui.hotkey("command", "l")

def pause_video():
    pyautogui.press("space")

def refresh_page():
    pyautogui.hotkey("command", "r")

def close_tab():
    pyautogui.hotkey("command", "w")

def new_tab():
    pyautogui.hotkey("command", "t")

def next_tab():
    pyautogui.hotkey("command", "shift", "bracketright")

def prev_tab():
    pyautogui.hotkey("command", "shift", "bracketleft")

def go_back():
    pyautogui.hotkey("command", "left")

def go_forward():
    pyautogui.hotkey("command", "right")

def zoom_in():
    pyautogui.hotkey("command", "equal")

def zoom_out():
    pyautogui.hotkey("command", "minus")

def zoom_reset():
    pyautogui.hotkey("command", "0")

def find_on_page():
    pyautogui.hotkey("command", "f")

def reload_page_n(n: int):
    for _ in range(n):
        refresh_page()
        time.sleep(0.8)


# ── Scroll ────────────────────────────────────────────────────────────────────

def scroll_up(amount: int = 500):   pyautogui.scroll(amount)
def scroll_down(amount: int = 500): pyautogui.scroll(-amount)
def scroll_top():    pyautogui.hotkey("command", "up")
def scroll_bottom(): pyautogui.hotkey("command", "down")
def page_up():       pyautogui.press("pageup")
def page_down():     pyautogui.press("pagedown")


# ── Clipboard / Typing ───────────────────────────────────────────────────────

def copy():       pyautogui.hotkey("command", "c")
def paste():      pyautogui.hotkey("command", "v")
def cut():        pyautogui.hotkey("command", "x")
def undo():       pyautogui.hotkey("command", "z")
def redo():       pyautogui.hotkey("command", "shift", "z")
def select_all(): pyautogui.hotkey("command", "a")
def save_file():  pyautogui.hotkey("command", "s")

def press_enter():  pyautogui.press("enter")
def press_escape(): pyautogui.press("escape")
def press_key(key: str): pyautogui.press(key)

def type_text(text: str, press_enter_after: bool = False):
    if not text:
        return
    if _PYPERCLIP:
        pyperclip.copy(text)
        time.sleep(0.1)
        paste()
    else:
        pyautogui.write(str(text), interval=0.03)
    if press_enter_after:
        time.sleep(0.1)
        pyautogui.press("enter")

def write_on_screen(text: str):
    type_text(text)


# ── System ────────────────────────────────────────────────────────────────────

def take_screenshot():
    pyautogui.hotkey("command", "shift", "3")

def lock_screen():
    subprocess.run(["pmset", "displaysleepnow"])

def open_system_settings():
    subprocess.Popen(["open", "-a", "System Settings"])

def open_file_explorer():
    subprocess.Popen(["open", str(Path.home())])

def sleep_display():
    subprocess.run(["pmset", "displaysleepnow"])

def restart_computer():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to restart'])

def shutdown_computer():
    subprocess.run(["osascript", "-e", 'tell application "System Events" to shut down'])

def dark_mode():
    subprocess.run(["osascript", "-e",
        'tell app "System Events" to tell appearance preferences to set dark mode to not dark mode'])

def toggle_wifi():
    subprocess.run(["networksetup", "-setairportpower", "en0", "toggle"])

def spotlight():
    pyautogui.hotkey("command", "space")


# ── Action Map ────────────────────────────────────────────────────────────────

ACTION_MAP = {
    "volume_up":               volume_up,
    "volume_down":             volume_down,
    "mute":                    volume_mute,
    "unmute":                  volume_mute,
    "volume_increase":         volume_up,
    "volume_decrease":         volume_down,
    "increase_volume":         volume_up,
    "decrease_volume":         volume_down,
    "turn_up_volume":          volume_up,
    "turn_down_volume":        volume_down,
    "louder":                  volume_up,
    "quieter":                 volume_down,
    "silence":                 volume_mute,
    "toggle_mute":             volume_mute,
    "brightness_up":           brightness_up,
    "brightness_down":         brightness_down,
    "increase_brightness":     brightness_up,
    "decrease_brightness":     brightness_down,
    "brighter":                brightness_up,
    "dimmer":                  brightness_down,
    "dim_screen":              brightness_down,
    "brighten_screen":         brightness_up,
    "sleep_display":           sleep_display,
    "turn_off_screen":         sleep_display,
    "screen_off":              sleep_display,
    "display_off":             sleep_display,
    "screen_sleep":            sleep_display,
    "monitor_off":             sleep_display,
    "turn_off_monitor":        sleep_display,
    "pause_video":             pause_video,
    "play_video":              pause_video,
    "pause":                   pause_video,
    "play":                    pause_video,
    "toggle_play":             pause_video,
    "stop_video":              pause_video,
    "resume_video":            pause_video,
    "close_app":               close_app,
    "close_window":            close_window,
    "quit_app":                close_app,
    "exit_app":                close_app,
    "kill_app":                close_app,
    "full_screen":             full_screen,
    "fullscreen":              full_screen,
    "toggle_fullscreen":       full_screen,
    "minimize":                minimize_window,
    "minimize_window":         minimize_window,
    "maximize":                maximize_window,
    "maximize_window":         maximize_window,
    "restore_window":          maximize_window,
    "snap_left":               snap_left,
    "snap_right":              snap_right,
    "window_left":             snap_left,
    "window_right":            snap_right,
    "switch_window":           switch_window,
    "alt_tab":                 switch_window,
    "next_window":             switch_window,
    "show_desktop":            show_desktop,
    "desktop":                 show_desktop,
    "hide_windows":            show_desktop,
    "task_manager":            open_task_manager,
    "open_task_manager":       open_task_manager,
    "activity_monitor":        open_task_manager,
    "task_view":               open_task_view,
    "mission_control":         open_task_view,
    "screenshot":              take_screenshot,
    "take_screenshot":         take_screenshot,
    "capture_screen":          take_screenshot,
    "lock_screen":             lock_screen,
    "lock":                    lock_screen,
    "open_settings":           open_system_settings,
    "system_settings":         open_system_settings,
    "settings":                open_system_settings,
    "preferences":             open_system_settings,
    "file_explorer":           open_file_explorer,
    "open_explorer":           open_file_explorer,
    "finder":                  open_file_explorer,
    "open_finder":             open_file_explorer,
    "open_files":              open_file_explorer,
    "spotlight":               spotlight,
    "open_spotlight":          spotlight,
    "restart":                 restart_computer,
    "restart_computer":        restart_computer,
    "reboot":                  restart_computer,
    "reboot_computer":         restart_computer,
    "shutdown":                shutdown_computer,
    "shut_down":               shutdown_computer,
    "power_off":               shutdown_computer,
    "turn_off_computer":       shutdown_computer,
    "dark_mode":               dark_mode,
    "toggle_dark_mode":        dark_mode,
    "night_mode":              dark_mode,
    "toggle_wifi":             toggle_wifi,
    "wifi":                    toggle_wifi,
    "wifi_toggle":             toggle_wifi,
    "focus_search":            focus_search,
    "address_bar":             focus_search,
    "url_bar":                 focus_search,
    "refresh_page":            refresh_page,
    "reload_page":             refresh_page,
    "reload":                  refresh_page,
    "refresh":                 refresh_page,
    "close_tab":               close_tab,
    "new_tab":                 new_tab,
    "open_tab":                new_tab,
    "next_tab":                next_tab,
    "prev_tab":                prev_tab,
    "previous_tab":            prev_tab,
    "go_back":                 go_back,
    "back":                    go_back,
    "go_forward":              go_forward,
    "forward":                 go_forward,
    "zoom_in":                 zoom_in,
    "zoom_out":                zoom_out,
    "zoom_reset":              zoom_reset,
    "reset_zoom":              zoom_reset,
    "find_on_page":            find_on_page,
    "search_page":             find_on_page,
    "scroll_up":               scroll_up,
    "scroll_down":             scroll_down,
    "scroll_top":              scroll_top,
    "scroll_bottom":           scroll_bottom,
    "top_of_page":             scroll_top,
    "bottom_of_page":          scroll_bottom,
    "page_up":                 page_up,
    "page_down":               page_down,
    "copy":                    copy,
    "paste":                   paste,
    "cut":                     cut,
    "undo":                    undo,
    "redo":                    redo,
    "select_all":              select_all,
    "save":                    save_file,
    "save_file":               save_file,
    "enter":                   press_enter,
    "press_enter":             press_enter,
    "escape":                  press_escape,
    "press_escape":            press_escape,
    "cancel":                  press_escape,
}


def _detect_action(description: str) -> dict:
    """Uses Gemini to detect user intent from any language."""
    from core.llm import generate

    available = ", ".join(sorted(ACTION_MAP.keys())) + ", volume_set, type_text, write_on_screen, reload_n, press_key"

    prompt = f"""The user wants to control their macOS computer. Detect their intent.

User said (in any language): "{description}"

Available actions: {available}

Return ONLY valid JSON:
{{"action": "action_name", "value": null_or_value}}

Examples:
- "turn up the volume" -> {{"action": "volume_up", "value": null}}
- "set volume to 60" -> {{"action": "volume_set", "value": 60}}
- "close the app" -> {{"action": "close_app", "value": null}}
- "type hello world" -> {{"action": "type_text", "value": "hello world"}}
- "take a screenshot" -> {{"action": "screenshot", "value": null}}
- "open finder" -> {{"action": "finder", "value": null}}
- "toggle dark mode" -> {{"action": "dark_mode", "value": null}}
- "press f5" -> {{"action": "press_key", "value": "f5"}}

IMPORTANT:
- Always return one of the available actions listed above.
- If the user's intent is clear but uses different wording, map it to the closest action.
- Never invent new action names not in the available list.
- Return ONLY the JSON object, no explanation, no markdown."""

    try:
        text = generate(prompt, gemini_model="gemini-2.5-flash-lite")
        text = __import__("re").sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
        return json.loads(text)
    except Exception as e:
        print(f"[Settings] Intent detection failed: {e}")
        return {"action": description.lower().replace(" ", "_"), "value": None}


def computer_settings(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
) -> str:
    if not _PYAUTOGUI:
        return "pyautogui is not installed. Run: pip install pyautogui"

    params      = parameters or {}
    raw_action  = params.get("action", "").strip()
    description = params.get("description", "").strip()
    value       = params.get("value", None)

    if not raw_action and description:
        detected   = _detect_action(description)
        raw_action = detected.get("action", "")
        if value is None:
            value = detected.get("value")

    action = raw_action.lower().strip().replace(" ", "_").replace("-", "_")

    if not action:
        return "No action could be determined, sir."

    print(f"[Settings] Action: {action}  Value: {value}")

    if action == "volume_set":
        try:
            volume_set(int(value or 50))
            return f"Volume set to {value}%."
        except Exception as e:
            return f"Could not set volume: {e}"

    if action in ("type_text", "write_on_screen", "type", "write"):
        text = str(value or params.get("text", ""))
        if not text:
            return "No text provided to type, sir."
        enter_after = bool(params.get("press_enter", False))
        type_text(text, press_enter_after=enter_after)
        return f"Typed: {text[:60]}"

    if action == "press_key":
        key = str(value or params.get("key", ""))
        if not key:
            return "No key specified, sir."
        press_key(key)
        return f"Pressed: {key}"

    if action in ("reload_n", "refresh_n", "reload_page_n"):
        try:
            n = int(value or 1)
            reload_page_n(n)
            return f"Reloaded page {n} time{'s' if n > 1 else ''}."
        except Exception as e:
            return f"Could not reload: {e}"

    if action in ("scroll_up", "scroll_down"):
        try:
            amount = int(value or 500)
            scroll_up(amount) if action == "scroll_up" else scroll_down(amount)
            return f"Scrolled {'up' if action == 'scroll_up' else 'down'}."
        except Exception as e:
            return f"Scroll failed: {e}"

    func = ACTION_MAP.get(action)
    if not func:
        return f"Unknown action: '{raw_action}', sir."

    try:
        func()
        return f"Done: {action}."
    except Exception as e:
        return f"Action failed ({action}): {e}"
