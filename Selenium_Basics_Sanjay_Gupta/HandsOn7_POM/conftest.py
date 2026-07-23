"""
=========================================================
Hands-On 7
conftest.py

Shared pytest fixtures

Provides:
1. Chrome Driver
2. Base URL
3. Screenshot on Failure
=========================================================
"""

import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# =========================================================
# Driver Fixture
# =========================================================

@pytest.fixture(scope="function")
def driver(request):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.maximize_window()
    driver.implicitly_wait(10)

    request.node.driver = driver

    yield driver

    driver.quit()


# =========================================================
# Base URL Fixture
# =========================================================

@pytest.fixture(scope="session")
def base_url():

    return "https://www.testmuai.com/selenium-playground/"



# =========================================================
# Screenshot on Failure
# =========================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = getattr(item, "driver", None)

        if driver:

            os.makedirs("screenshots", exist_ok=True)

            filename = os.path.join(
                "screenshots",
                f"{item.name}_failure.png"
            )

            try:

                driver.save_screenshot(filename)

                print(f"\nScreenshot Saved : {filename}")

            except Exception:

                pass
