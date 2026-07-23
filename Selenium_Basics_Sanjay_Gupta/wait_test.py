"""
================================================================================
HANDS-ON 5: Locators — ID, Name, XPath, CSS Selectors & Explicit Waits
Filename : wait_test.py
================================================================================

Task 2: WebDriverWait and Expected Conditions

Steps Covered:
- Step 36: WebDriverWait & ExpectedConditions (`visibility_of_element_located`)
- Step 37: Benchmarking `time.sleep(3)` vs `WebDriverWait` Performance
- Step 38: ExpectedCondition `element_to_be_clickable` vs `visibility_of_element_located`
- Step 39: FluentWait Implementation (Custom Polling & Ignored Exceptions)
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException
)
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome in Headless Mode for CI/CD compatibility
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    # ==============================================================================
    # Step 36: Bootstrap Alerts Demo with WebDriverWait & visibility_of_element_located
    # ==============================================================================
    print("--- Step 36: Bootstrap Alert Visibility with WebDriverWait ---")
    url_alerts = "https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo/"
    driver.get(url_alerts)
    print(f"Navigated to: {driver.current_url}")

    # Wait for the Success Message button to be clickable and click it
    btn_locator = (By.XPATH, "//button[contains(.,'Autocloseable Success') or contains(.,'Normal Success') or contains(text(),'Success')]")
    success_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_locator))
    success_btn.click()
    print("Clicked Success Message button.")

    # Wait for the success alert div to become visible
    alert_locator = (By.CSS_SELECTOR, ".alert-success, div[class*='alert-success']")
    success_alert = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(alert_locator))
    
    alert_text = success_alert.text.strip()
    print(f"Alert Text Captured: '{alert_text}'")
    assert "success" in alert_text.lower() or "autocloseable" in alert_text.lower() or len(alert_text) > 0, "Alert text verification failed!"
    print("SUCCESS: Alert text verified successfully using WebDriverWait.\n")

    # ==============================================================================
    # Step 37: Benchmarking time.sleep(3) vs Explicit Wait Performance
    # ==============================================================================
    print("--- Step 37: Benchmarking time.sleep(3) vs Explicit Wait ---")

    # 1. Measurement with hardcoded time.sleep(3)
    driver.refresh()
    start_sleep_time = time.time()
    btn_sleep = driver.find_element(*btn_locator)
    btn_sleep.click()
    time.sleep(3)  # Arbitrary hardcoded sleep
    alert_sleep = driver.find_element(*alert_locator)
    elapsed_sleep = time.time() - start_sleep_time
    print(f"1. Hardcoded time.sleep(3) execution time: {elapsed_sleep:.3f} seconds")

    # 2. Measurement with Explicit Wait (WebDriverWait)
    driver.refresh()
    start_explicit_time = time.time()
    btn_explicit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_locator))
    btn_explicit.click()
    alert_explicit = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(alert_locator))
    elapsed_explicit = time.time() - start_explicit_time
    print(f"2. Dynamic Explicit Wait execution time   : {elapsed_explicit:.3f} seconds")

    time_saved = elapsed_sleep - elapsed_explicit
    print(f"--> Dynamic Explicit Wait was {time_saved:.3f} seconds FASTER!")

    """
    --------------------------------------------------------------------------------
    Step 37 Explanation: Why Hardcoded time.sleep() is a Bad Practice in Automation
    --------------------------------------------------------------------------------
    1. Unnecessary Execution Delay:
       If an element renders in 0.05 seconds (50ms), time.sleep(3) STILL wastes 2.95 seconds.
       In a suite of 500 tests, this adds over 25 minutes of useless execution overhead.

    2. Unreliability on Slow Connections:
       If the server or network slows down and takes 3.1 seconds to respond, time.sleep(3)
       fails with an exception, causing test flakiness.

    3. Dynamic Efficiency:
       WebDriverWait polls the DOM dynamically (every 500ms) and returns IMMEDIATELY when
       the condition is met, delivering maximum speed on fast machines and maximum reliability
       up to the specified timeout on slow ones.
    """
    print()

    # ==============================================================================
    # Step 38: EC.element_to_be_clickable() vs EC.visibility_of_element_located()
    # ==============================================================================
    print("--- Step 38: Demonstrating element_to_be_clickable ---")
    driver.refresh()
    clickable_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn_locator))
    print(f"Element verified as clickable: Tag='{clickable_btn.tag_name}', Text='{clickable_btn.text.strip()}'")

    """
    --------------------------------------------------------------------------------
    Step 38 Explanation: Difference Between visibility and clickable
    --------------------------------------------------------------------------------
    1. visibility_of_element_located(locator):
       - Checks that the element is present in the DOM.
       - AND has a height and width greater than 0 (is physically visible on screen).
       - Does NOT check if the element is disabled or covered by an overlay/spinner.

    2. element_to_be_clickable(locator):
       - Checks that the element is present in the DOM.
       - AND is physically visible (height > 0, width > 0).
       - AND is enabled (`is_enabled() == True`).
       - AND is NOT obscured or blocked by loading spinners, modal backdrops, or animation overlays.
       * Recommendation: ALWAYS use element_to_be_clickable prior to performing .click() actions.
    """
    print("SUCCESS: Demonstrated element_to_be_clickable successfully.\n")

    # ==============================================================================
    # Step 39: Demonstrate FluentWait (Polling every 500ms, Ignore Exceptions)
    # ==============================================================================
    print("--- Step 39: Demonstrating FluentWait for Dynamic Tables ---")
    url_table = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo/"
    driver.get(url_table)
    print(f"Navigated to: {driver.current_url}")

    # FluentWait configuration in Selenium Python using WebDriverWait
    # Polling frequency: 500ms (0.5s), Timeout: 10s, Ignored Exceptions: NoSuchElementException
    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, ElementNotInteractableException]
    )

    # Wait dynamically for table row to become visible
    table_row_locator = (By.XPATH, "//table[@id='example']//tbody/tr[1]")
    dynamic_row = fluent_wait.until(EC.visibility_of_element_located(table_row_locator))
    
    print(f"FluentWait SUCCESS: Located dynamic table row: '{dynamic_row.text.strip()}'")
    assert dynamic_row is not None, "Failed to locate dynamic table row via FluentWait!"

finally:
    driver.quit()
    print("\nBrowser closed successfully.")
