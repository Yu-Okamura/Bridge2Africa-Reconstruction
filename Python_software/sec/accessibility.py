"""
Compatible with Python 3.12
Last MOD: 4/19/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.
"""

from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np


def find_accessibility_score(link):
    """
    Evaluates the accessibility score of a given webpage using the WAVE web accessibility evaluation tool.
    :param link: URL of the webpage to be evaluated.
    :return: Accessibility status string indicating if the website is accessible or not.
    """
    result = ""
    driver_ = webdriver.Chrome(ChromeDriverManager().install())
    try:
        driver_.minimize_window()
        wave_link = "https://wave.webaim.org/report#/"
        driver_.get(wave_link + link)

        # Wait for the page to fully load
        time.sleep(10)

        # Get the page's source
        page_html = driver_.page_source
        page_soup = soup(page_html, "html.parser")

        # Parse accessibility scores from the WAVE results
        sidebar = page_soup.find(id="sidebar_wrapper")
        tabs = sidebar.find(id="tabs")
        summary = tabs.find(id="summary")
        numbers = summary.find(id="numbers")

        error = int(numbers.find(id="error").find('span').get_text())
        contrast = int(numbers.find(id="contrast").find('span').get_text())
        alert = int(numbers.find(id="alert").find('span').get_text())
        feature = int(numbers.find(id="feature").find('span').get_text())
        structure = int(numbers.find(id="structure").find('span').get_text())
        aria = int(numbers.find(id="aria").find('span').get_text())

        # Convert to accessibility score values
        scores = np.zeros(6, dtype=float)
        scores[0] = 1 - error / 500  # Error weight
        scores[1] = contrast / 5     # Contrast weight
        scores[2] = 1 - alert / 2000 # Alert weight
        scores[3] = feature / 100    # Feature weight
        scores[4] = structure / 500  # Structure weight
        scores[5] = aria / 50 if aria != 304 else aria / 500

        mean_score = np.mean(scores)

        # Determine accessibility based on the mean score
        if mean_score >= 0.5:
            result = "This website is accessible"
            print("This website is accessible")
        else:
            result = "This website is not accessible"
            print("This website is not accessible")

        driver_.close()

    except Exception as e:
        result = f"Cannot analyze website: {str(e)}"
        driver_.close()

    return result
