import subprocess
import sys

print("Installing requirements...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

print("Installing Playwright browsers...")
subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

print("\n Setup complete! Run 'python main.py' to start MARK XXXV.")
print("\nIMPORTANT: Grant Accessibility permissions to your terminal app:")
print("  System Settings -> Privacy & Security -> Accessibility")
print("  Add Terminal.app (or iTerm2, etc.)")
