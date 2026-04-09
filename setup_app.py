"""
py2app build script for MARK XXXV macOS
Usage: python setup_app.py py2app
"""
from setuptools import setup

APP = ['main.py']
APP_NAME = 'MARK XXXV'

DATA_FILES = [
    ('core', ['core/prompt.txt']),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'app_icon.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleIdentifier': 'com.nixfred.mark-xxxv',
        'CFBundleVersion': '0.9.0',
        'CFBundleShortVersionString': '0.9',
        'NSMicrophoneUsageDescription': 'MARK XXXV needs microphone access for voice commands.',
        'NSCameraUsageDescription': 'MARK XXXV needs camera access for visual analysis.',
        'NSAppleEventsUsageDescription': 'MARK XXXV uses AppleScript to control system settings and send messages.',
        'NSScreenCaptureUsageDescription': 'MARK XXXV needs screen capture for visual analysis.',
        'LSMinimumSystemVersion': '12.0',
        'NSHighResolutionCapable': True,
    },
    'packages': [
        'google', 'google.genai', 'google.generativeai',
        'cv2', 'numpy', 'PIL', 'mss',
        'sounddevice', 'pyautogui', 'pyperclip',
        'requests', 'bs4',
        'duckduckgo_search', 'psutil', 'send2trash',
        'youtube_transcript_api',
        'AppKit', 'Quartz', 'objc',
        'websockets', 'httpx', 'certifi',
        'actions', 'agent', 'core', 'memory',
    ],
    'includes': [
        'tkinter', 'sqlite3', 'json', 'asyncio',
        'threading', 'subprocess', 'pathlib',
    ],
    'excludes': [
        'test', 'unittest', 'distutils',
        'setuptools', 'pkg_resources',
        'playwright',
    ],
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
