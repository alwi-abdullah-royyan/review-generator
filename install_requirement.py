import subprocess
import sys

def install_requirements():
    try:
        import pyperclip
    except ImportError:
        print("pyperclip is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])

    try:
        import groq
    except ImportError:
        print("groq is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])

# Call this function at the beginning of your script to ensure dependencies are installed
install_requirements()
