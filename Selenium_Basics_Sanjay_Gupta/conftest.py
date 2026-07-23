"""
================================================================================
HANDS-ON 6: Running Selenium Tests with pytest — Fixtures, Assertions & Reporting
Filename : conftest.py
================================================================================

Task 2: Pytest Fixtures, Base URL Constant & Screenshot Failure Hook

Contains:
1. Function-scoped Chrome Driver Fixture (setup & teardown via yield)
2. Session-scoped base_url Fixture (Step 48)
3. Failure Screenshot Hook (Step 46)
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ==============================================================================
# Step 41: Function-scoped Chrome Driver Fixture
# ==============================================================================
@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped fixture: Creates a fresh Chrome browser instance for every test.
    Ensures complete test isolation (no shared cookies, session state, or leftover DOM state).
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Setup: Initialize Chrome WebDriver via ChromeDriverManager
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    browser.implicitly_wait(10)

    # Attach driver instance to test item node for screenshot hooks
    request.node.driver = browser

    # Yield control to the test function
    yield browser

    # Teardown: Quit browser session clean after test execution
    browser.quit()


# ==============================================================================
# Step 48: Session-scoped Base URL Fixture Constant
# ==============================================================================
@pytest.fixture(scope="session")
def base_url():
    """Returns the base target URL constant for LambdaTest Selenium Playground."""
    return "https://www.lambdatest.com/selenium-playground/"


# ==============================================================================
# Step 46: Pytest Hook for Screenshot Capture on Test Failure
# ==============================================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hooks into test execution phases to automatically capture a screenshot
    whenever a test fails during the execution ('call') phase.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            # Create screenshot filename based on test item name
            screenshot_path = os.path.join("screenshots", f"{item.name}_failure.png")
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\n[FAILURE HOOK] Captured failure screenshot saved to: {screenshot_path}")
            except Exception as e:
                print(f"\n[FAILURE HOOK] Failed to capture screenshot: {e}")
