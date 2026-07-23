"""
=========================================================
Hands-On 7
Pytest Test Cases using Page Object Model

No driver.find_element() calls are used here.
=========================================================
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage



# =====================================================
# Question 55 / Step 52
# =====================================================

def test_simple_form_submission(driver, base_url):

    page = SimpleFormPage(driver)

    page.navigate_to(base_url + "simple-form-demo/")

    page.enter_message("Hello Selenium")

    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


# =====================================================
# Question 56 / Step 53
# =====================================================

def test_checkbox_demo(driver, base_url):

    page = CheckboxPage(driver)

    page.navigate_to(base_url + "checkbox-demo/")

    page.check_option(0)

    assert page.is_option_checked(0)

    page.uncheck_option(0)

    assert page.is_option_checked(0) == False


# =====================================================
# Question 56 / Step 54
# =====================================================

def test_dropdown_selection(driver, base_url):

    page = DropdownPage(driver)

    page.navigate_to(base_url + "select-dropdown-demo/")

    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


# =====================================================
# Question 57
# =====================================================

def test_input_form_submit(driver, base_url):

    page = InputFormPage(driver)

    page.navigate_to(base_url + "input-form-demo/")

    page.fill_form(

        "Shivatharani",

        "shivatharani@gmail.com",

        "Cognizant",

        "Chennai"

    )

    page.submit_form()

    assert "Submitted" in page.get_success_message()


if __name__ == "__main__":
    import os
    import pytest
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    sys.exit(pytest.main(["-v", __file__, "--html=report.html", "--self-contained-html"]))
