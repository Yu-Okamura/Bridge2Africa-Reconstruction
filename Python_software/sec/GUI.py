"""
Compatible with Python 3.12
Last MOD: 3/25/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.
"""

import tkinter as tk
import pyttsx3
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget)

from util import read_shortcut, write_json
from shortcuts import *
import json

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

class ShortcutsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600+10+20")
        self.root.configure(bg='peach puff')
        self.root.title('Shortcuts')

        self.label = tk.Label(self.root, text="Shortcuts", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        self.create_buttons()

        engine.say("Opening Shortcuts")
        engine.runAndWait()
        self.root.mainloop()

    def create_buttons(self):
        """Helper function to create all the GUI buttons"""
        buttons_info = [
            ("Start to Translate \nto Braille", self.TranslateToBraille, 100, 100),
            ("Enable Braille Display", self.EnableBrailleDisplay, 350, 100),
            ("Toggle Navigation", self.ToggleNavigation, 600, 100),
            ("Accessibility", self.Accessibility, 100, 250),
            ("Index Up", self.IndexUp, 350, 250),
            ("Index Down", self.IndexDown, 600, 250),
            ("Text to Speech", self.TextToSpeech, 100, 400),
            ("Quit Translation", self.QuitTranslation, 350, 400),
            ("Continue Translation", self.ContinueTranslation, 600, 400)
        ]

        for text, command, x, y in buttons_info:
            tk.Button(self.root, text=text, font=('Arial', 14), command=command).place(x=x, y=y, height=100, width=200)

        self.backBtn = tk.Button(self.root, text="< Settings", font=('Arial', 12), command=self.ReturnToSettings)
        self.backBtn.place(x=10, y=10, height=50, width=100)

    def TranslateToBraille(self):
        self.root.destroy()
        TranslateToBraille()

    def EnableBrailleDisplay(self):
        self.root.destroy()
        EnableBrailleDisplay()

    def ToggleNavigation(self):
        self.root.destroy()
        ToggleNavigation()

    def Accessibility(self):
        self.root.destroy()
        Accessibility()

    def IndexUp(self):
        self.root.destroy()
        IndexUp()

    def IndexDown(self):
        self.root.destroy()
        IndexDown()

    def TextToSpeech(self):
        self.root.destroy()
        TextToSpeech()

    def QuitTranslation(self):
        self.root.destroy()
        QuitTranslation()

    def ContinueTranslation(self):
        self.root.destroy()
        ContinueTranslation()

    def ReturnToSettings(self):
        self.root.destroy()
        SettingsGUI()


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600+10+20")
        self.root.configure(bg='peach puff')
        self.root.title('Main Menu')

        self.label = tk.Label(self.root, text="Main Menu", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        self.create_main_buttons()

        engine.say("Opening Main Menu")
        engine.runAndWait()
        self.root.mainloop()

    def create_main_buttons(self):
        """Helper function to create main menu buttons"""
        buttons_info = [
            ("Settings", self.OpenSettings, 350, 100),
            ("Open Browser", self.OpenBrowser, 350, 250),
            ("Modes", self.OpenModes, 350, 400)
        ]

        for text, command, x, y in buttons_info:
            tk.Button(self.root, text=text, font=('Arial', 14), command=command).place(x=x, y=y, height=100, width=200)

    def OpenSettings(self):
        self.root.destroy()
        SettingsGUI()

    def OpenBrowser(self):
        if not getBrowserOpen():
            on_triggered()

    def OpenModes(self):
        self.root.destroy()
        ModesGUI()


class SettingsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600+10+20")
        self.root.configure(bg='peach puff')
        self.root.title('Settings')

        self.label = tk.Label(self.root, text="Settings", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        self.create_settings_buttons()

        engine.say("Opening Settings")
        engine.runAndWait()
        self.root.mainloop()

    def create_settings_buttons(self):
        """Helper function to create settings buttons"""
        buttons_info = [
            ("Shortcuts", self.OpenShortcuts, 350, 100),
            ("Speech Speed", self.OpenSpeeds, 350, 250)
        ]

        for text, command, x, y in buttons_info:
            tk.Button(self.root, text=text, font=('Arial', 14), command=command).place(x=x, y=y, height=100, width=200)

        self.backBtn = tk.Button(self.root, text="< Main Menu", font=('Arial', 12), command=self.ReturnToMain)
        self.backBtn.place(x=10, y=10, height=50, width=100)

    def OpenShortcuts(self):
        self.root.destroy()
        ShortcutsGUI()

    def ReturnToMain(self):
        self.root.destroy()
        MainMenu()

    def OpenSpeeds(self):
        self.root.destroy()
        SpeechSpeedGUI()


class ModesGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600+10+20")
        self.root.configure(bg='peach puff')
        self.root.title('Modes')

        self.label = tk.Label(self.root, text="Modes", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        self.create_modes_buttons()

        engine.say("Opening Modes")
        engine.runAndWait()
        self.root.mainloop()

    def create_modes_buttons(self):
        """Helper function to create modes buttons"""
        buttons_info = [
            ("Assistantive Mode", None, 350, 100),
            ("Individual Mode\n(Automatic)", None, 350, 250),
            ("Individual Mode\n(Manual)", None, 350, 400)
        ]

        for text, command, x, y in buttons_info:
            tk.Button(self.root, text=text, font=('Arial', 14), command=command).place(x=x, y=y, height=100, width=200)

    def ReturnToMain(self):
        self.root.destroy()
        MainMenu()


# Example helper classes for specific tasks
class TranslateToBraille:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class EnableBrailleDisplay:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class ToggleNavigation:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class Accessibility:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class IndexUp:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class IndexDown:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class TextToSpeech:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class QuitTranslation:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class ContinueTranslation:
    def __init__(self):
        # Similar to the ShortcutsGUI class
        pass

class SpeechSpeedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600+10+20")
        self.root.configure(bg='peach puff')
        self.root.title('Speed Settings')

        self.label = tk.Label(self.root, text="Speech Speed", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        self.create_speed_buttons()

        engine.say("Opening Speech Speed Settings")
        engine.runAndWait()
        self.root.mainloop()

    def create_speed_buttons(self):
        """Helper function to create buttons for speech speed settings"""
        buttons_info = [
            ("Slow", self.SlowSpeed, 100, 250, 'tomato'),
            ("Medium", self.MediumSpeed, 350, 250, 'gold'),
            ("Fast", self.FastSpeed, 600, 250, 'SpringGreen2')
        ]

        for text, command, x, y, color in buttons_info:
            tk.Button(self.root, text=text, font=('Arial', 14), command=command, bg=color).place(x=x, y=y, height=200, width=200)

    def SlowSpeed(self):
        self.update_speed(30)

    def MediumSpeed(self):
        self.update
