"""
Compatible with Python 3.12
Last MOD: 4/30/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.
"""

from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import pyttsx3
import keyboard
import time
import serial
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from parse_website import get_headers, describe_hierarchy
from util import read_shortcut, write_json
from driver import send_data, clear_cache, arduino, webinfo_to_arduino
from accessibility import find_accessibility_score

# Global variables
INDEX = 1
TITLE = 0
HEADER = 0
P = 0
LINKS = 0
TITLE_INDEX = 0
HEADER_INDEX = 0
P_INDEX = 0
LINKS_INDEX = 0
CONTAINER = ""
NAV_ID = 0
NAV = ["headers", "title", "paragraph", "links"]
NAV_NODE = 0
CONTAINER_BRAILLE = ""
BROWSER_OPEN = False
driver = None
ser = None
cache = []
engine = None
IS_BROWSER_OPEN = False

def buttons():
    """
    Function to handle serial data input for triggering speech or hierarchy actions.
    """
    global ser
    flag = True

    while True:
        ser_data = ser.readline().decode().strip()
        if ser_data == '1' and flag:
            print('Triggering speech...')
            on_triggered_speak()
            flag = False
        elif ser_data == '2' and flag:
            print('Describing hierarchy...')
            hierarchy()
            flag = False

        if ser_data == '0':
            flag = True

def getBrowserOpen():
    """
    Returns the current state of the browser (whether open or not).
    :return: Boolean indicating if the browser is open.
    """
    global IS_BROWSER_OPEN
    return IS_BROWSER_OPEN

def close_driver():
    """
    Closes the browser if it's open.
    """
    global driver
    global IS_BROWSER_OPEN
    if IS_BROWSER_OPEN:
        driver.quit()
        IS_BROWSER_OPEN = False

def intialize_speech():
    """
    Initializes the text-to-speech engine with the user-configured speed.
    """
    global engine
    shortcut = read_shortcut()
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    rate_of_speech = rate + int(shortcut.get("speed", 0))
    engine.setProperty('rate', rate_of_speech)

def intialize_arduino():
    """
    Initializes the serial connection to the Arduino.
    """
    global ser
    try:
        ser = serial.Serial('COM3', 9600)
        print("Arduino connection established.")
    except serial.SerialException as e:
        print(f"Failed to initialize Arduino: {e}")

def track_webbrowser():
    """
    Tracks the currently opened browser and updates navigation pointers when switching pages.
    """
    global CONTAINER, TITLE, HEADER, P, LINKS, TITLE_INDEX, HEADER_INDEX, P_INDEX, LINKS_INDEX, IS_BROWSER_OPEN

    current_website = None

    while True:
        try:
            windows = driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[1])
                driver.close()
                driver.switch_to.window(windows[0])
            if not windows:
                IS_BROWSER_OPEN = False
            else:
                IS_BROWSER_OPEN = True

            if driver.current_url != current_website:
                current_website = driver.current_url
                uClient = urlopen(Request(current_website))
                page_html = uClient.read()
                uClient.close()

                page_soup = soup(page_html, "html.parser")
                CONTAINER = page_soup

                TITLE_INDEX = HEADER_INDEX = P_INDEX = LINKS_INDEX = 0
                result = describe_hierarchy(CONTAINER)

                TITLE, HEADER, P, LINKS = result
                time.sleep(1)
                NAV_ID = 0
                navigation()

        except Exception as e:
            print(f"Error tracking web browser: {e}")

def page_navigation_minus():
    """
    Decrements the index of the current navigation setting (e.g., headers, title, etc.).
    """
    global NAV_ID, TITLE_INDEX, HEADER_INDEX, P_INDEX, LINKS_INDEX, engine

    engine.stop()

    if NAV_ID == 0:
        HEADER_INDEX = max(0, HEADER_INDEX - 1)
        engine.say(f"Headers {HEADER_INDEX}")
    elif NAV_ID == 1:
        TITLE_INDEX = max(0, TITLE_INDEX - 1)
        engine.say(f"Title {TITLE_INDEX}")
    elif NAV_ID == 2:
        P_INDEX = max(0, P_INDEX - 1)
        engine.say(f"Paragraph {P_INDEX}")
    elif NAV_ID == 3:
        LINKS_INDEX = max(0, LINKS_INDEX - 1)
        engine.say(f"Links {LINKS_INDEX}")

    engine.runAndWait()

def page_navigation_add():
    """
    Increments the index of the current navigation setting (e.g., headers, title, etc.).
    """
    global NAV_ID, TITLE_INDEX, HEADER_INDEX, P_INDEX, LINKS_INDEX, TITLE, HEADER, P, LINKS, engine

    engine.stop()

    if NAV_ID == 0:
        HEADER_INDEX = (HEADER_INDEX + 1) % HEADER
        engine.say(f"Headers {HEADER_INDEX}")
    elif NAV_ID == 1:
        TITLE_INDEX = (TITLE_INDEX + 1) % TITLE
        engine.say(f"Title {TITLE_INDEX}")
    elif NAV_ID == 2:
        P_INDEX = (P_INDEX + 1) % P
        engine.say(f"Paragraph {P_INDEX}")
    elif NAV_ID == 3:
        LINKS_INDEX = (LINKS_INDEX + 1) % LINKS
        engine.say(f"Links {LINKS_INDEX}")

    engine.runAndWait()

def hierarchy():
    """
    Describes the hierarchy of the current webpage, including the number of titles, headers, paragraphs, and links.
    """
    global CONTAINER, TITLE, HEADER, P, LINKS, engine

    engine.stop()
    result = describe_hierarchy(CONTAINER)

    engine.say(f"Current website: {driver.current_url}")
    prompt = (f"There are {TITLE} Titles, {HEADER} Headers, {P} Paragraphs, and {LINKS} Links on this page")
    engine.say(prompt)
    engine.runAndWait()

def on_triggered_speak():
    """
    Speaks out the current navigation pointer based on index and navigation settings.
    """
    prompt = return_prompt()
    engine.stop()
    engine.say(prompt)
    engine.runAndWait()

def return_prompt():
    """
    Returns the current navigation pointer's text based on the navigation index.
    """
    global NAV, NAV_ID, TITLE_INDEX, HEADER_INDEX, P_INDEX, LINKS_INDEX, CONTAINER

    result = get_headers(CONTAINER, NAV[NAV_ID])
    prompt = ""

    if NAV_ID == 0:
        prompt = result[HEADER_INDEX] if HEADER_INDEX < len(result) else ""
    elif NAV_ID == 1:
        prompt = result[TITLE_INDEX] if TITLE_INDEX < len(result) else ""
    elif NAV_ID == 2:
        prompt = result[P_INDEX] if P_INDEX < len(result) else ""
    elif NAV_ID == 3:
        prompt = result[LINKS_INDEX] if LINKS_INDEX < len(result) else ""

    return prompt

def on_triggered():
    """
    Initializes the web browser and opens Google as the default page.
    """
    global driver, engine, BROWSER_OPEN

    engine.say("Opening new Web browser")
    engine.runAndWait()

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()

    engine.say("Current website: google.com")
    engine.runAndWait()
    driver.get("https://www.google.com/")
    BROWSER_OPEN = True

def on_triggered_read():
    """
    Starts braille read by translating web content to braille and sending it to Arduino.
    """
    global ser, CONTAINER_BRAILLE, engine, cache

    result = return_prompt().lower()
    data = read_json()

    engine.say("Translating to braille")
    engine.runAndWait()

    webinfo_to_arduino(ser, engine, result, data, cache)

def navigation():
    """
    Switches to the next navigation setting (headers, title, paragraph, links).
    """
    global NAV_ID, NAV, TITLE_INDEX, HEADER_INDEX, P_INDEX, LINKS_INDEX, engine

    engine.stop()

    NAV_ID = (NAV_ID + 1) % len(NAV)
    engine.say(NAV[NAV_ID])
    engine.runAndWait()

    page_navigation_add()

def web_accessibility():
    """
    Evaluates and announces the accessibility of the current webpage.
    """
    global NAV_ID, CONTAINER, engine

    if NAV[NAV_ID] == "links":
        result = get_headers(CONTAINER, NAV[NAV_ID])
        link = result[LINKS_INDEX]
        score = find_accessibility_score(link)
        engine.say(score)
        engine.runAndWait()
