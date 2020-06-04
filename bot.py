"""The type racer bot class."""

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


class Bot:
    # The text of the current typing race.
    typing_content: str

    def __init__(self):
        """Initialize the Chrome web driver."""
        self.driver = webdriver.Chrome(executable_path=settings.WEB_DRIVER_PATH)

    def run(self):
        """The main function that runs the whole process."""
        self._init_race()
        self.typing_content = self._get_typing_content()
        print(self.typing_content)

        # wait for the countdown
        txt_input = self.driver.find_element_by_class_name("txtInput")
        while True:
            if "txtInput-unfocused" not in txt_input.get_attribute("class"):
                break
            time.sleep(0.5)

        self._type_content(settings.WPM)

    def _init_race(self):
        """Sign in and start a race."""

        self.driver.get(settings.SITE_ADDR)

        # Wait for sign-in button to load.
        try:
            sign_in_btn = WebDriverWait(self.driver, settings.WD_WAIT_DELAY) \
                .until(EC.presence_of_element_located((By.LINK_TEXT, "Sign In")))
            sign_in_btn.click()
        except TimeoutException:
            print("Loading sign-in button took too much time.")

        # Sign in.
        self.driver.find_element_by_name("username").send_keys(settings.USR_NAME)
        self.driver.find_element_by_name("password").send_keys(settings.PWD)
        self.driver.find_element_by_class_name("gwt-Button").click()

        # Start race.
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("[title^='Keyboard shortcut: Ctrl+Alt+I']").click()

    def _get_typing_content(self) -> str:
        """Fetch and return the typing content"""
        time.sleep(0.5)
        elms = self.driver.find_elements_by_css_selector("[unselectable^='on']")

        res = ""
        for elm in elms:
            # Get textContent attribute to avoid selenium auto trimming leading and ending white spaces
            res += elm.get_attribute("textContent")

        return res

    def _type_content(self, wpm: int):
        """Type the content with the given wpm."""
        char_delay = self._get_input_delay(wpm)
        txt_input = self.driver.find_element_by_class_name("txtInput")
        for c in self.typing_content:
            time.sleep(char_delay)
            txt_input.send_keys(c)

    def _get_input_delay(self, wpm: int) -> float:
        """Return calculated input delay in seconds between each char input based on wpm."""
        word_count = self.typing_content.count(' ') + 1
        char_count = self.typing_content.__len__()
        tot_time = word_count / wpm * 60

        return tot_time / char_count
