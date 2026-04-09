# MARK XXXV — macOS Port

**A complete macOS port of the [Mark XXXV](https://github.com/FatihMakes/Mark-XXXV) voice assistant.**

The original project by [@FatihMakes](https://github.com/FatihMakes) is an incredible JARVIS-style AI assistant — but it only runs on Windows. This fork rewrites every Windows-specific module to run natively on macOS using osascript, AVFoundation, cron, and native Apple APIs.

---

## Why This Exists

The original Mark XXXV repo has thousands of stars and one of the most common questions is "does this work on Mac?" It didn't. Now it does.

This isn't a thin compatibility shim — it's a full rewrite of 16 files. Every `winreg` call, every `pycaw` volume control, every `schtasks` reminder, every `CAP_DSHOW` camera capture has been replaced with macOS-native equivalents. The Windows-only dependencies (`pycaw`, `comtypes`, `win10toast`, `pygetwindow`, `pywinauto`) are gone entirely.

---

## What It Does

You run it, you talk, your Mac does things. Gemini's Live Audio API handles the full voice loop — your mic streams audio to Gemini, Gemini decides what to do, calls tools that control your Mac, and speaks back through your speakers. No separate speech-to-text or text-to-speech — it's native audio end-to-end.

**Capabilities:**
- **Voice control** — Speak naturally in any language. Gemini handles intent detection.
- **App launching** — `open -a` with Spotlight fallback. 40+ app aliases mapped.
- **System control** — Volume (osascript), brightness (System Events key codes), dark mode, Wi-Fi, lock, restart, shutdown.
- **Screen & camera analysis** — Screenshots via `mss`, webcam via `AVFoundation`, sent to Gemini Vision for analysis. JARVIS describes what it sees.
- **Browser automation** — Full Playwright-based control. Opens your default browser, navigates, clicks, fills forms, searches.
- **Reminders** — `cron` + `osascript` notification dialogs. Self-cleaning scripts.
- **Messaging** — WhatsApp, Telegram, Instagram via pyautogui + **native iMessage via AppleScript** (Mac-exclusive feature).
- **Terminal commands** — Natural language → zsh commands via Gemini. Hardcoded shortcuts for common tasks (disk space, battery, processes).
- **Persistent memory** — Remembers your name, preferences, relationships across sessions in a local JSON file.
- **YouTube** — Search, play, summarize transcripts, get video info, trending videos.
- **File management** — List, create, move, copy, organize desktop by type or date.
- **Code generation** — Write, edit, explain, and run code files.
- **Weather, flights, web search** — API-based tools that work cross-platform.

---

## Quick Start

```bash
git clone https://github.com/nixfred/Mark-XXXV.git
cd Mark-XXXV
pip install -r requirements.txt
playwright install
python main.py
```

1. First launch shows a setup screen — paste your free [Gemini API key](https://aistudio.google.com/apikey)
2. Grant **Accessibility permissions**: System Settings → Privacy & Security → Accessibility → add your terminal app
3. Talk to JARVIS

### Requirements

- macOS 12+ (Monterey or newer)
- Python 3.11 or 3.12
- Microphone
- Free Gemini API key

---

## What Changed from the Original

This port touched 16 of 19 Python files. Here's what was replaced:

| What | Windows (Original) | macOS (This Fork) |
|------|-------------------|-------------------|
| Volume | `pycaw` + COM interfaces | `osascript set volume` |
| Brightness | Win Action Center hotkey | System Events key codes 144/145 |
| App launch | `pyautogui.press("win")` + search | `open -a` + Spotlight (`Cmd+Space`) |
| Reminders | Windows Task Scheduler XML + `schtasks` | `crontab` + `osascript display notification` |
| Camera | `cv2.CAP_DSHOW` (DirectShow) | `cv2.CAP_AVFOUNDATION` |
| Screen capture | `PIL.ImageGrab` | `mss` |
| Browser detection | Windows Registry (`winreg`) | `defaults read LSHandlers` |
| Wallpaper | `ctypes.windll.user32.SystemParametersInfoW` | `osascript tell Finder set desktop picture` |
| Terminal commands | `cmd.exe` / PowerShell | `zsh` via `/bin/zsh` |
| Window focus | PowerShell `WScript.Shell.AppActivate` | `osascript tell app to activate` |
| Keyboard shortcuts | `Ctrl+` everywhere | `Command+` everywhere |
| Messaging | WhatsApp/Telegram only | + **native iMessage** via AppleScript |
| Game updates | Steam/Epic via Registry + pywinauto | Removed (not applicable on Mac) |
| User-Agent strings | Windows NT 10.0 | Macintosh; Intel Mac OS X |
| Notifications | `win10toast` | `osascript display dialog` |
| Process listing | `tasklist` / `taskkill` | `ps aux` / `lsof` |

**Removed dependencies:** `pycaw`, `comtypes`, `win10toast`, `pygetwindow`, `pywinauto`

---

## The UI

The tkinter HUD runs identically on macOS — animated JARVIS face, rotating rings, pulse effects, status indicators (LISTENING / SPEAKING / THINKING / MUTED), scrolling conversation log, text input bar, and mute button (F4).

---

## Limitations

- **No wake word** — Always listening when unmuted (uses API quota)
- **No offline mode** — Requires internet for Gemini API
- **Accessibility permissions required** — macOS blocks keyboard/mouse automation without explicit permission
- **No Steam/Epic game management** — Windows-only feature, removed in this fork
- **Free tier rate limits** — Gemini API has request limits (upgradeable via Google AI Studio)

---

## Credits

- **Original project:** [@FatihMakes](https://github.com/FatihMakes) — built the entire Mark XXXV architecture, UI, tool system, and Gemini Live Audio integration. All the hard engineering work.
- **macOS port:** [@nixfred](https://github.com/nixfred) — rewrote all platform-specific modules for macOS, added iMessage support, replaced all Windows dependencies.

## License

Personal and non-commercial use only. Licensed under **Creative Commons BY-NC 4.0**.
