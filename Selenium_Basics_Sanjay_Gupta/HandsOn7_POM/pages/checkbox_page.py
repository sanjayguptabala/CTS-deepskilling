"""
=========================================================
Hands-On 7
Checkbox Page

Contains checkbox actions.

No assertions here.
=========================================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class CheckboxPage(BasePage):

    def get_checkbox(self, index):

        # Wait until checkboxes are present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
        )

        checkboxes = self.driver.find_elements(

            By.CSS_SELECTOR,

            "input[type='checkbox']"

        )

        return checkboxes[index]

    def check_option(self, index):

        checkbox = self.get_checkbox(index)

        # Wait until the checkbox is clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(checkbox))

        if not checkbox.is_selected():

            checkbox.click()

    def uncheck_option(self, index):

        checkbox = self.get_checkbox(index)

        # Wait until the checkbox is clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(checkbox))

        if checkbox.is_selected():

            checkbox.click()

    def is_option_checked(self, index):

        checkbox = self.get_checkbox(index)

        return checkbox.is_selected()
