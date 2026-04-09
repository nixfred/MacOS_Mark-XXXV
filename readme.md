# MARK XXXV — macOS Edition

### Voice-Controlled AI Assistant for Mac — Powered by Gemini

A real-time voice AI that can hear, see, understand, and control your Mac.
Zero subscriptions (unless you want to increase requests via Google AI Studio).

> **macOS fork** of [FatihMakes/Mark-XXXV](https://github.com/FatihMakes/Mark-XXXV) — the original Windows version. Full credit to [@FatihMakes](https://www.youtube.com/@FatihMakes) for the incredible original project.

---

## What It Does

Speak naturally — JARVIS listens, understands context, responds with a human-like voice, and executes tasks on your Mac automatically.

**Core capabilities:**
* **Real-time voice interaction** — Natural conversation with instant response
* **Mac control** — Launch apps, manage files, execute terminal commands
* **Visual awareness** — Screen analysis and webcam understanding via Gemini Vision
* **Persistent memory** — Learns your name, preferences, and context across sessions
* **iMessage support** — Send texts natively via AppleScript
* **Browser automation** — Full Playwright-based web control
* **Reminders** — Cron-based scheduling with native macOS notifications

---

## Quick Start

```bash
git clone https://github.com/nixfred/Mark-XXXV.git
cd Mark-XXXV
pip install -r requirements.txt
playwright install
python main.py
```

Enter your free Gemini API key on first launch.

### Important: Accessibility Permissions

For voice commands that control your Mac (typing, clicking, keyboard shortcuts), you must grant Accessibility permissions:

**System Settings → Privacy & Security → Accessibility** → Add your terminal app (Terminal.app, iTerm2, etc.)

---

## Requirements

* **macOS 12+** (Monterey or newer)
* **Python 3.11 or 3.12**
* Microphone
* Free [Gemini API key](https://aistudio.google.com/apikey)

---

## What's Different from the Windows Version

| Feature | Windows Original | macOS Fork |
|---------|-----------------|------------|
| Volume control | pycaw/COM | osascript |
| App launching | Win key search | `open -a` + Spotlight |
| Reminders | Task Scheduler | cron + osascript notifications |
| Messaging | WhatsApp/Telegram | + native iMessage support |
| Camera | DirectShow | AVFoundation |
| Terminal | CMD/PowerShell | zsh |
| Game updates | Steam/Epic registry | Removed (not applicable) |
| Screen capture | ImageGrab | mss (cross-platform) |
| Wallpaper | ctypes.windll | osascript + Finder |

---

## Voice Commands

| You Say | What Happens |
|---------|-------------|
| "Open Spotify" | Launches via `open -a Spotify` |
| "Set volume to 40" | `osascript` volume control |
| "What's on my screen?" | Screenshot → Gemini Vision → spoken analysis |
| "Search for reviews" | Playwright browser automation |
| "Remind me at 3pm" | cron job + macOS notification |
| "Send a message to John" | WhatsApp, Telegram, or iMessage |
| "Toggle dark mode" | System Events AppleScript |
| "Take a screenshot" | Cmd+Shift+3 |
| "Lock the screen" | `pmset displaysleepnow` |

---

## License

Personal and non-commercial use only.
Licensed under **Creative Commons BY-NC 4.0**.

Original project by [@FatihMakes](https://github.com/FatihMakes) — a 17-year-old building a real JARVIS.
macOS port by [@nixfred](https://github.com/nixfred).
