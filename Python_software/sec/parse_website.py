"""
Compatible with Python 3.12
Last MOD: 4/4/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.
"""

from bs4 import BeautifulSoup as soup
import re

def get_headers(container, nav_type):
    """
    HTML parses all headers, page title, paragraphs, or links based on the provided navigation type.
    :param container: HTML container to parse.
    :param nav_type: Type of navigation (headers, title, paragraph, links).
    :return: List of parsed text elements.
    """
    result = []

    if nav_type == "headers":
        for headlines in container.find_all(["h1", "h2", "h3", "h4", "h5"]):
            result.append(headlines.get_text(strip=True))

    elif nav_type == "title":
        title = container.find_all("title")
        for i in title:
            result.append(i.get_text(strip=True))

    elif nav_type == "paragraph":
        for div in container.find_all('p'):
            result.append(div.get_text(strip=True))

    elif nav_type == "links":
        for link in container.find_all('a', href=True):
            href = link['href']
            if href.startswith("http"):
                result.append(href)

    return result

def describe_hierarchy(container):
    """
    HTML parses all headers, page title, paragraphs, and links, and counts the number of each.
    :param container: HTML container to parse.
    :return: A list with counts of titles, headers, paragraphs, and links respectively.
    """
    title = [title.get_text(strip=True) for title in container.find_all("title")]
    header = [headline.get_text(strip=True) for headline in container.find_all(["h1", "h2", "h3", "h4", "h5"])]
    paragraph = [para.get_text(strip=True) for para in container.find_all('p')]
    links = [link['href'] for link in container.find_all('a', href=True) if link['href'].startswith("http")]

    return [len(title), len(header), len(paragraph), len(links)]
