"""
A typeracer.com typing bot implemented using Python.

I am writing this silly project this because I am so bored staying at home for COVID-19.
"""

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import settings

__author__ = "Qiwen Hua"
__version__ = "0.1.0"
__email__ = "qiwen.hua@mail.utoronto.ca"


def init_race():
    """Sign in and start a race."""

    driver.get(settings.SITE_ADDR)

    # Wait for sign-in button to load.
    try:
        sign_in_btn = WebDriverWait(driver, settings.WD_WAIT_DELAY) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, 'gwt-Anchor')))
        sign_in_btn.click()
    except TimeoutException:
        print("Loading sign-in button took too much time.")

    # Sign in.
    driver.find_element_by_name("username").send_keys(settings.USR_NAME)
    driver.find_element_by_name("password").send_keys(settings.PWD)
    driver.find_element_by_class_name("gwt-Button").click()

    # Start race.
    time.sleep(0.5)
    driver.find_element_by_css_selector("[title^='Keyboard shortcut: Ctrl+Alt+I']").click()


def get_typing_content() -> str:
    """Fetch and return the typing content"""
    time.sleep(0.5)
    elms = driver.find_elements_by_css_selector("[unselectable^='on']")

    res = ""
    for elm in elms:
        # Get textContent attribute to avoid selenium auto trimming leading and ending white spaces
        res += elm.get_attribute("textContent")

    return res


def type_content(wpm: int):
    """"""
    pass


if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=settings.WEB_DRIVER_PATH)
    init_race()
