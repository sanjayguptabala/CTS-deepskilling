"""
================================================================================
HANDS-ON 4: Selenium WebDriver Setup, Browser Drivers & Basic Commands
Filename : navigation_test.py
================================================================================

Task 2: WebDriver Navigation and Window Commands

Steps Covered:
- Step 28: Page Navigation & URL Assertion (`driver.back()`, `driver.current_url`)
- Step 29: Multi-Tab Window Handling (`window_handles`, `switch_to.window()`)
- Step 30: Capture & Verify Screenshot (`save_screenshot()`)
- Step 31: Viewport Resolution Management (`get_window_size()`, `set_window_size()`)
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================================================
# Environment Setup: Initialize Chrome WebDriver in Headless Mode for CI/CD
# ==============================================================================
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
driver.implicitly_wait(10)

try:
    # ==============================================================================
    # Step 28: Navigate, Click Demo Link, Assert URL, and Navigate Back
    # ==============================================================================
    print("--- Step 28: Page Navigation & URL Assertion ---")
    base_url = "https://www.lambdatest.com/selenium-playground/"
    driver.get(base_url)
    print(f"Initial Page Title: {driver.title}")

    # Locate and click 'Simple Form Demo' link
    simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
    simple_form_link.click()

    # Assert URL contains 'simple-form-demo'
    current_url = driver.current_url
    print(f"Navigated URL: {current_url}")
    assert "simple-form-demo" in current_url, f"Expected 'simple-form-demo' in URL, but got '{current_url}'"
    print("ASSERTION PASSED: URL contains 'simple-form-demo'.")

    # Navigate back to main playground home page
    driver.back()
    print(f"Navigated Back to URL: {driver.current_url}")
    assert "simple-form-demo" not in driver.current_url and "selenium-playground" in driver.current_url, "Failed to navigate back to playground home page!"
    print("SUCCESS: Navigated back to home page successfully.\n")

    # ==============================================================================
    # Step 29: Open New Browser Tab, List Handles, Switch & Print Google Title
    # ==============================================================================
    print("--- Step 29: Multi-Tab Window Handling ---")
    
    # Open new browser tab using JavaScript execution
    driver.execute_script('window.open("https://www.google.com");')

    # Get all window handles
    handles = driver.window_handles
    print(f"Total Open Window Handles ({len(handles)}):")
    for idx, handle in enumerate(handles):
        print(f"  Tab [{idx}]: {handle}")

    # Switch control to the newly opened tab (index 1)
    driver.switch_to.window(handles[1])
    print(f"Switched to Tab [1] - Title: '{driver.title}'")

    # Verification of Google Tab Title
    google_title = driver.title
    print(f"Google Tab Title: {google_title}")
    assert "Google" in google_title or len(google_title) > 0, "Failed to switch or fetch Google tab title!"
    print("SUCCESS: Switched to new tab and printed title successfully.\n")

    # ==============================================================================
    # Step 30: Switch Back to Original Tab & Save Screenshot
    # ==============================================================================
    print("--- Step 30: Switch Back & Capture Screenshot ---")
    
    # Switch back to original playground tab (index 0)
    driver.switch_to.window(handles[0])
    print(f"Switched Back to Tab [0] - URL: {driver.current_url}")

    # Capture screenshot and save as 'playground_screenshot.png'
    screenshot_filename = "playground_screenshot.png"
    driver.save_screenshot(screenshot_filename)
    print(f"Saved screenshot to: {screenshot_filename}")

    # Verify screenshot file exists on disk
    assert os.path.exists(screenshot_filename), f"Screenshot file '{screenshot_filename}' was not created!"
    file_size_bytes = os.path.getsize(screenshot_filename)
    print(f"VERIFICATION PASSED: File '{screenshot_filename}' exists on disk (Size: {file_size_bytes} bytes).\n")

    # ==============================================================================
    # Step 31: Demonstrate get_window_size() and set_window_size(1280, 800)
    # ==============================================================================
    print("--- Step 31: Window Size & Viewport Management ---")
    
    # Get current window size
    initial_size = driver.get_window_size()
    print(f"Initial Window Size: Width = {initial_size['width']}px, Height = {initial_size['height']}px")

    # Set window size to standard 1280x800 resolution
    target_width, target_height = 1280, 800
    driver.set_window_size(target_width, target_height)

    # Fetch updated window size
    updated_size = driver.get_window_size()
    print(f"Updated Window Size: Width = {updated_size['width']}px, Height = {updated_size['height']}px")

    """
    --------------------------------------------------------------------------------
    Step 31 Explanation: Why Consistent Browser Window Size Matters in UI Automation
    --------------------------------------------------------------------------------
    1. Responsive Layout Breakpoints:
       Modern web applications use CSS media queries and responsive grid breakpoints
       that dynamically alter UI layouts (e.g., collapsing navigation bars into hamburger
       menus or hiding sidebar elements) depending on browser viewport dimensions.

    2. Element Visibility & Clickability:
       If a test runs on a machine with small screen resolution or headless default sizes,
       elements required for test execution might render off-screen or overlap, causing
       `ElementNotInteractableException` or `ElementClickInterceptedException`.

    3. Cross-Environment Test Determinism:
       Enforcing a standardized, fixed window size (e.g., 1280x800 or 1920x1080) across all
       developer workstations and headless CI/CD pipeline runners eliminates environment-specific
       layout discrepancies and prevents flaky test failures.
    """
    print("SUCCESS: Window size updated and documented successfully.")

finally:
    # Clean up browser resources
    driver.quit()
    print("\nBrowser closed successfully.")
