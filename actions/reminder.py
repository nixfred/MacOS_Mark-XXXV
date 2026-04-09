# actions/reminder.py
# macOS — Reminders via cron + osascript notification

import subprocess
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def reminder(
    parameters: dict,
    response: str | None = None,
    player=None,
    session_memory=None
) -> str:
    """
    Sets a timed reminder using cron + osascript notification on macOS.

    parameters:
        - date    (str) YYYY-MM-DD
        - time    (str) HH:MM
        - message (str)

    Returns a result string — Live API voices it automatically.
    """

    date_str = parameters.get("date")
    time_str = parameters.get("time")
    message  = parameters.get("message", "Reminder")

    if not date_str or not time_str:
        return "I need both a date and a time to set a reminder."

    try:
        target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

        if target_dt <= datetime.now():
            return "That time is already in the past."

        safe_message = message.replace('"', '').replace("'", "").replace("\\", "").strip()[:200]

        # Create a self-deleting notification script
        script_dir = Path.home() / ".mark-reminders"
        script_dir.mkdir(exist_ok=True)

        task_name    = f"mark_reminder_{target_dt.strftime('%Y%m%d_%H%M')}"
        script_path  = script_dir / f"{task_name}.sh"

        # Script plays sound, shows notification, then cleans up
        script_code = f'''#!/bin/bash
# MARK Reminder — auto-generated
afplay /System/Library/Sounds/Glass.aiff &
osascript -e 'display notification "{safe_message}" with title "MARK Reminder" sound name "Glass"'
osascript -e 'display dialog "{safe_message}" with title "MARK Reminder" buttons {{"OK"}} default button "OK" with icon note'

# Self-cleanup: remove this script and its cron entry
crontab -l 2>/dev/null | grep -v "{task_name}" | crontab -
rm -f "{script_path}"
'''
        script_path.write_text(script_code)
        os.chmod(script_path, 0o755)

        # Add cron entry
        minute = target_dt.minute
        hour   = target_dt.hour
        day    = target_dt.day
        month  = target_dt.month

        cron_line = f"{minute} {hour} {day} {month} * {script_path} # {task_name}"

        # Get existing crontab, append new entry
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True
        )
        existing = result.stdout.strip()
        new_crontab = f"{existing}\n{cron_line}\n" if existing else f"{cron_line}\n"

        # Install updated crontab
        proc = subprocess.run(
            ["crontab", "-"],
            input=new_crontab, capture_output=True, text=True
        )

        if proc.returncode != 0:
            err = proc.stderr.strip()
            print(f"[Reminder] crontab failed: {err}")
            script_path.unlink(missing_ok=True)
            return "I couldn't schedule the reminder due to a system error."

        if player:
            player.write_log(f"[reminder] set for {date_str} {time_str}")

        return f"Reminder set for {target_dt.strftime('%B %d at %I:%M %p')}."

    except ValueError:
        return "I couldn't understand that date or time format."

    except Exception as e:
        return f"Something went wrong while scheduling the reminder: {str(e)[:80]}"
