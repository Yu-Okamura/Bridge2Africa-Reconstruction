"""
Compatible with Python 3.12
Last MOD: 5/3/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.

Additional installation:
pip install beautifulsoup4 selenium numpy webdriver-manager
pip install --upgrade beautifulsoup4
pip install pyserial keyboard
"""

import os
import threading
import sys
from GUI import MainMenu
from shortcuts import read_shortcut
from driver import intialize_arduino, track_webbrowser, buttons, close_driver
from accessibility import web_accessibility
import keyboard

THREADS = []

def main():
    """
    Main loop: Initializes speech, threads functions, and sets up shortcuts.
    """
    try:
        # Initialize speech engine
        intialize_speech()

        # Start browser tracking in a separate thread
        t = threading.Thread(target=track_webbrowser, daemon=True)
        THREADS.append(t)

        # Start button input handling in a separate thread
        t = threading.Thread(target=buttons, daemon=True)
        THREADS.append(t)

        # Load shortcuts from JSON
        shortcut = read_shortcut()

        # Register keyboard shortcuts
        keyboard.add_hotkey(shortcut.get("readBraille", ""), on_triggered_read)
        keyboard.add_hotkey(shortcut.get("navigation", ""), navigation)
        keyboard.add_hotkey(shortcut.get("indexPlus", ""), page_navigation_add)
        keyboard.add_hotkey(shortcut.get("indexMinus", ""), page_navigation_minus)
        keyboard.add_hotkey(shortcut.get("activateArduino", ""), intialize_arduino)
        keyboard.add_hotkey(shortcut.get("accessibility", ""), web_accessibility)
        keyboard.add_hotkey(shortcut.get("speak", ""), on_triggered_speak)
        keyboard.add_hotkey(shortcut.get("hierarchy", ""), hierarchy)

        # Start all threads
        for t in THREADS:
            t.start()

        # Launch GUI main menu
        MainMenu()

        # Close browser and other resources
        close_driver()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
