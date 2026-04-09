# actions/send_message.py
# macOS messaging — WhatsApp, Instagram, Telegram
# Uses Spotlight (Cmd+Space) to launch apps and Cmd-based shortcuts

import time
import subprocess
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.08


def _open_app(app_name: str) -> bool:
    """Opens an app via macOS open -a, falls back to Spotlight."""
    try:
        result = subprocess.run(
            ["open", "-a", app_name],
            capture_output=True, timeout=8
        )
        if result.returncode == 0:
            time.sleep(2.0)
            return True
    except Exception:
        pass

    # Fallback: Spotlight
    try:
        pyautogui.hotkey("command", "space")
        time.sleep(0.5)
        pyautogui.write(app_name, interval=0.04)
        time.sleep(0.6)
        pyautogui.press("enter")
        time.sleep(2.0)
        return True
    except Exception as e:
        print(f"[SendMessage] Could not open {app_name}: {e}")
        return False


def _send_whatsapp(receiver: str, message: str) -> str:
    """Sends a WhatsApp message via the macOS desktop app."""
    try:
        if not _open_app("WhatsApp"):
            return "Could not open WhatsApp."

        time.sleep(1.5)

        # Search for contact
        pyautogui.hotkey("command", "f")
        time.sleep(0.4)
        pyautogui.hotkey("command", "a")
        pyautogui.write(receiver, interval=0.04)
        time.sleep(1.0)

        pyautogui.press("enter")
        time.sleep(0.8)

        # Type and send
        pyautogui.write(message, interval=0.03)
        time.sleep(0.2)
        pyautogui.press("enter")

        return f"Message sent to {receiver} via WhatsApp."

    except Exception as e:
        return f"WhatsApp error: {e}"


def _send_instagram(receiver: str, message: str) -> str:
    """Sends an Instagram DM via browser."""
    try:
        import webbrowser

        webbrowser.open("https://www.instagram.com/direct/new/")
        time.sleep(3.5)

        pyautogui.write(receiver, interval=0.05)
        time.sleep(1.5)

        pyautogui.press("down")
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(0.5)

        for _ in range(3):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(1.5)

        pyautogui.write(message, interval=0.04)
        time.sleep(0.2)
        pyautogui.press("enter")

        return f"Message sent to {receiver} via Instagram."

    except Exception as e:
        return f"Instagram error: {e}"


def _send_telegram(receiver: str, message: str) -> str:
    """Sends a Telegram message via the macOS desktop app."""
    try:
        if not _open_app("Telegram"):
            return "Could not open Telegram."

        time.sleep(1.5)

        pyautogui.hotkey("command", "f")
        time.sleep(0.4)
        pyautogui.write(receiver, interval=0.04)
        time.sleep(1.0)
        pyautogui.press("enter")
        time.sleep(0.8)

        pyautogui.write(message, interval=0.03)
        time.sleep(0.2)
        pyautogui.press("enter")

        return f"Message sent to {receiver} via Telegram."

    except Exception as e:
        return f"Telegram error: {e}"


def _find_contact(name: str) -> dict | None:
    """
    Search macOS Contacts database directly via sqlite3.
    Returns {"name": "Full Name", "phone": "+1...", "email": "..."} or None.
    Fuzzy matches — "crystal nicks" finds "Crystal Nix".
    """
    import sqlite3
    from pathlib import Path

    name_parts = name.lower().strip().split()
    if not name_parts:
        return None

    # Find all AddressBook databases
    ab_dir = Path.home() / "Library" / "Application Support" / "AddressBook"
    db_paths = list(ab_dir.glob("Sources/*/AddressBook-v22.abcddb"))
    db_paths.append(ab_dir / "AddressBook-v22.abcddb")

    best_match = None
    best_score = 0

    for db_path in db_paths:
        if not db_path.exists():
            continue
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row

            # Search by first name part (most distinctive)
            first = name_parts[0]
            rows = conn.execute("""
                SELECT r.ZFIRSTNAME, r.ZLASTNAME, r.Z_PK,
                       (SELECT p.ZFULLNUMBER FROM ZABCDPHONENUMBER p
                        WHERE p.ZOWNER = r.Z_PK LIMIT 1) as phone,
                       (SELECT e.ZADDRESS FROM ZABCDEMAILADDRESS e
                        WHERE e.ZOWNER = r.Z_PK LIMIT 1) as email
                FROM ZABCDRECORD r
                WHERE LOWER(r.ZFIRSTNAME) LIKE ?
                   OR LOWER(r.ZLASTNAME) LIKE ?
            """, (f"%{first}%", f"%{first}%")).fetchall()

            for row in rows:
                first_name = row["ZFIRSTNAME"] or ""
                last_name = row["ZLASTNAME"] or ""
                full_name = f"{first_name} {last_name}".strip()
                fn_lower = full_name.lower()
                fn_parts = set(fn_lower.split())

                # Score the match
                if fn_lower == " ".join(name_parts):
                    score = 100  # Exact match
                elif all(any(np in fp or fp in np for fp in fn_parts) for np in name_parts):
                    score = 90  # All parts fuzzy match
                else:
                    overlap = sum(1 for np in name_parts
                                  if any(np in fp or fp in np for fp in fn_parts))
                    score = overlap * 40

                if score > best_score:
                    best_score = score
                    best_match = {
                        "name": full_name,
                        "phone": (row["phone"] or "").strip(),
                        "email": (row["email"] or "").strip(),
                    }

            conn.close()
        except Exception as e:
            print(f"[SendMessage] DB search error ({db_path.name}): {e}")
            continue

    if best_match and best_score >= 40:
        print(f"[SendMessage] Contact: '{name}' -> '{best_match['name']}' (score: {best_score})")
        return best_match

    print(f"[SendMessage] No contact match for '{name}'")
    return None


def _send_imessage(receiver: str, message: str) -> str:
    """Sends an iMessage/SMS via macOS Messages app. Validates contact first."""
    try:
        # Look up the contact
        contact = _find_contact(receiver)

        if contact:
            actual_name = contact["name"]
            # Use phone number if available (most reliable for iMessage)
            target = contact["phone"] or contact["email"] or actual_name
            print(f"[SendMessage] iMessage to: {actual_name} ({target})")
        else:
            print(f"[SendMessage] No contact found for '{receiver}', using name as-is")
            actual_name = receiver
            target = receiver

        safe_msg = message.replace('"', '\\"')
        safe_target = target.replace('"', '\\"')

        # Try sending via phone number or email (direct AppleScript)
        if contact and (contact["phone"] or contact["email"]):
            script = f'''
tell application "Messages"
    set targetService to 1st account whose service type = iMessage
    set targetBuddy to participant "{safe_target}" of targetService
    send "{safe_msg}" to targetBuddy
end tell
'''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                return f"iMessage sent to {actual_name}."

        # Fallback: open Messages app, use contact name for search
        if not _open_app("Messages"):
            return "Could not open Messages."
        time.sleep(1.5)
        pyautogui.hotkey("command", "n")
        time.sleep(0.5)
        # Type the validated contact name
        pyautogui.write(actual_name, interval=0.04)
        time.sleep(1.0)
        # Select first suggestion
        pyautogui.press("down")
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(0.5)
        # Tab to message field and type
        pyautogui.press("tab")
        time.sleep(0.3)
        pyautogui.write(message, interval=0.03)
        pyautogui.press("enter")
        return f"Message sent to {actual_name} via Messages."

    except Exception as e:
        return f"iMessage error: {e}"


def _send_generic(platform: str, receiver: str, message: str) -> str:
    """For any other platform. Opens the app and tries search + send."""
    try:
        if not _open_app(platform):
            return f"Could not open {platform}."

        time.sleep(1.5)
        pyautogui.hotkey("command", "f")
        time.sleep(0.4)
        pyautogui.write(receiver, interval=0.04)
        time.sleep(1.0)
        pyautogui.press("enter")
        time.sleep(0.8)
        pyautogui.write(message, interval=0.03)
        time.sleep(0.2)
        pyautogui.press("enter")

        return f"Message sent to {receiver} via {platform}."

    except Exception as e:
        return f"{platform} error: {e}"


def send_message(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None
) -> str:
    """
    Called from main.py.

    Two-step flow:
      1. First call (confirmed=false): validates contact, returns match for confirmation
      2. Second call (confirmed=true): actually sends the message

    parameters:
        receiver     : Contact name to send to
        message_text : The message content
        platform     : whatsapp | instagram | telegram | imessage | <any app name>
        confirmed    : Must be true to actually send. Default: false
    """
    params       = parameters or {}
    receiver     = params.get("receiver", "").strip()
    message_text = params.get("message_text", "").strip()
    platform     = params.get("platform", "whatsapp").strip().lower()
    confirmed    = str(params.get("confirmed", "false")).lower() == "true"

    if not receiver:
        return "Please specify who to send the message to, sir."
    if not message_text:
        return "Please specify what message to send, sir."

    # Step 1: Validate contact and ask for confirmation
    if not confirmed:
        contact = _find_contact(receiver)
        if contact:
            return (
                f"I found {contact['name']} in your contacts"
                f"{' (' + contact['phone'] + ')' if contact['phone'] else ''}. "
                f"Should I send the message to {contact['name']}? Say yes to confirm or no to cancel."
            )
        else:
            return (
                f"I could not find '{receiver}' in your contacts, sir. "
                f"Please check the name and try again, or say the exact contact name."
            )

    # Step 2: Confirmed — actually send
    print(f"[SendMessage] CONFIRMED: {platform} -> {receiver}: {message_text[:40]}")
    if player:
        player.write_log(f"[msg] Sending to {receiver} via {platform}...")

    if "whatsapp" in platform or "wp" in platform or "wapp" in platform:
        result = _send_whatsapp(receiver, message_text)

    elif "instagram" in platform or "ig" in platform or "insta" in platform:
        result = _send_instagram(receiver, message_text)

    elif "telegram" in platform or "tg" in platform:
        result = _send_telegram(receiver, message_text)

    elif "imessage" in platform or "message" in platform or "sms" in platform or "text" in platform:
        result = _send_imessage(receiver, message_text)

    else:
        result = _send_generic(platform, receiver, message_text)

    print(f"[SendMessage] {result}")
    if player:
        player.write_log(f"[msg] {result}")

    return result
