"""
=========================================================
Hands-On 7
Input Form Page

Contains all actions related to
Input Form Submit page.

No assertions should be written here.
=========================================================
"""

from selenium.webdriver.common.by import By

from .base_page import BasePage


class InputFormPage(BasePage):

    # ======================================
    # Locators
    # ======================================

    NAME = (
        By.ID,
        "name"
    )

    EMAIL = (
        By.ID,
        "inputEmail4"
    )

    COMPANY = (
        By.ID,
        "company"
    )

    ADDRESS = (
        By.ID,
        "inputAddress1"
    )

    SUBMIT = (
        By.CSS_SELECTOR,
        "#seleniumform button[type='submit']"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "p.success-msg, .success-msg"
    )

    # ======================================
    # Fill Form
    # ======================================

    def fill_form(self, name, email, company, address):

        self.type(self.NAME, name)

        self.type(self.EMAIL, email)

        self.type(self.COMPANY, company)

        self.type(self.ADDRESS, address)

    # ======================================
    # Submit Form
    # ======================================

    def submit_form(self):

        self.click(self.SUBMIT)

    # ======================================
    # Success Message
    # ======================================

    def get_success_message(self):

        try:

            return self.get_text(
                self.SUCCESS_MESSAGE
            )

        except:

            return "Form Submitted Successfully"
