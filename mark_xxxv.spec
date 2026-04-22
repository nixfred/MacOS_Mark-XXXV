# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for MARK XXXV macOS
#
# BUILD PYTHON: 3.11.9 (python-build-standalone).
# DO NOT upgrade to 3.11.11+ — those ship Tcl/Tk 9.0, which crashes in
# Tk_AllocColorFromObj on aqua under the animated-canvas redraw loop (v0.9.2
# DiagnosticReports 074354). 3.11.9 ships Tcl/Tk 8.6.12 which is stable.
# The repo's .python-version pins this; uv respects it.
# To build:
#   uv venv --python 3.11.9 .venv-tk86
#   uv pip install --python .venv-tk86/bin/python -r requirements.txt pyinstaller
#   PBS=/Users/pi/.local/share/uv/python/cpython-3.11.9-macos-aarch64-none
#   TCL_LIBRARY=$PBS/lib/tcl8.6 TK_LIBRARY=$PBS/lib/tk8.6 \
#     .venv-tk86/bin/pyinstaller mark_xxxv.spec

import os
import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core/prompt.txt', 'core'),
        ('actions/*.py', 'actions'),
        ('agent/*.py', 'agent'),
        ('memory/*.py', 'memory'),
        ('memory/__init__.py', 'memory'),
        ('config/__init__.py', 'config'),
        ('config/api_keys.json', 'config'),
    ],
    hiddenimports=[
        'google.genai',
        'google.genai.live',
        'google.genai.types',
        'google.generativeai',
        'sounddevice',
        'mss', 'mss.tools',
        'cv2',
        'numpy',
        'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageDraw',
        'pyautogui', 'pyautogui._pyautogui_osx',
        'pyperclip',
        'requests', 'bs4',
        'duckduckgo_search',
        'psutil',
        'send2trash',
        'youtube_transcript_api',
        'websockets', 'websockets.asyncio',
        'httpx',
        'certifi',
        'AppKit', 'Quartz', 'objc',
        'tkinter',
        'sqlite3',
        'actions.browser_control',
        'actions.cmd_control',
        'actions.code_helper',
        'actions.computer_control',
        'actions.computer_settings',
        'actions.desktop',
        'actions.dev_agent',
        'actions.file_controller',
        'actions.flight_finder',
        'actions.game_updater',
        'actions.open_app',
        'actions.reminder',
        'actions.screen_processor',
        'actions.send_message',
        'actions.weather_report',
        'actions.web_search',
        'actions.youtube_video',
        'agent.error_handler',
        'agent.executor',
        'agent.planner',
        'agent.task_queue',
        'core.llm',
        'memory.memory_manager',
        'memory.config_manager',
        'config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['playwright', 'test', 'unittest'],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MARK XXXV',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MARK XXXV',
)

app = BUNDLE(
    coll,
    name='MARK XXXV.app',
    icon='app_icon.icns',
    bundle_identifier='com.nixfred.mark-xxxv',
    info_plist={
        'CFBundleName': 'MARK XXXV',
        'CFBundleDisplayName': 'MARK XXXV',
        'CFBundleVersion': '0.9.6',
        'CFBundleShortVersionString': '0.9.6',
        'NSMicrophoneUsageDescription': 'MARK XXXV needs microphone access for voice commands.',
        'NSCameraUsageDescription': 'MARK XXXV needs camera access for visual analysis.',
        'NSAppleEventsUsageDescription': 'MARK XXXV uses AppleScript to control system settings.',
        'LSMinimumSystemVersion': '12.0',
        'NSHighResolutionCapable': True,
    },
)
