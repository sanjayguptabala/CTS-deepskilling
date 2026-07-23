"""
=========================================================
Hands-On 7
Base Page

All page classes inherit from this class.

Common reusable Selenium methods are defined here.
=========================================================
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):

        self.driver = driver

    # =====================================================
    # Navigate
    # =====================================================

    def navigate_to(self, url):

        self.driver.get(url)

    # =====================================================
    # Get Browser Title
    # =====================================================

    def get_title(self):

        return self.driver.title

    # =====================================================
    # Wait for Element
    # =====================================================

    def wait_for_element(self, locator, timeout=10):

        return WebDriverWait(
            self.driver,
            timeout
        ).until(
            EC.visibility_of_element_located(locator)
        )

    # =====================================================
    # Click Element
    # =====================================================

    def click(self, locator):

        element = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(locator)
        )

        element.click()

    # =====================================================
    # Enter Text
    # =====================================================

    def type(self, locator, text):

        element = self.wait_for_element(locator)

        element.clear()

        element.send_keys(text)

    # =====================================================
    # Read Text
    # =====================================================

    def get_text(self, locator):

        element = self.wait_for_element(locator)

        return element.text

    # =====================================================
    # Read Input Value
    # =====================================================

    def get_value(self, locator):

        element = self.wait_for_element(locator)

        return element.get_attribute("value")

    # =====================================================
    # Check Selection
    # =====================================================

    def is_selected(self, locator):

        element = self.wait_for_element(locator)

        return element.is_selected()
