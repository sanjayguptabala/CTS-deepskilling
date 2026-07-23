"""
=========================================================
Hands-On 7
Dropdown Page

Contains all dropdown related methods.

No assertions should be written here.
=========================================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class DropdownPage(BasePage):

    # ======================================
    # Locator
    # ======================================

    DROPDOWN = (
        By.TAG_NAME,
        "select"
    )

    # ======================================
    # Select Day
    # ======================================

    def select_day(self, day_name):

        dropdown = self.wait_for_element(
            self.DROPDOWN
        )

        select = Select(dropdown)

        select.select_by_visible_text(day_name)

    # ======================================
    # Get Selected Day
    # ======================================

    def get_selected_day(self):

        dropdown = self.wait_for_element(
            self.DROPDOWN
        )

        select = Select(dropdown)

        return select.first_selected_option.text
