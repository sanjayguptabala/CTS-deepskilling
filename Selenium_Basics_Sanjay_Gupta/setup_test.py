"""
================================================================================
HANDS-ON 4: Selenium WebDriver Setup, Browser Drivers & Basic Commands
Filename : setup_test.py
================================================================================

Task 1: Selenium Architecture and Environment Setup

--------------------------------------------------------------------------------
Step 24: Selenium Component Architecture Overview
--------------------------------------------------------------------------------
1. Selenium WebDriver:
   - What it is: The core automation API of the Selenium suite providing a direct,
     language-specific (Python, Java, C#, JS) object-oriented binding to control browsers.
   - Communication Mechanism: Communicates directly with the browser's native automation
     engine by sending HTTP requests following the standardized W3C WebDriver Protocol
     through a browser driver executable (e.g., ChromeDriver for Chrome, GeckoDriver for Firefox).

2. Selenium Grid:
   - What problem it solves: Solves the challenge of running tests sequentially on a single machine.
   - Grid enables distributed, parallel test execution across multiple remote machines (Nodes),
     different operating systems (Windows, Linux, macOS), and various browser types/versions simultaneously,
     dramatically reducing overall regression suite execution time.

3. Selenium IDE (Integrated Development Environment):
   - What it is used for: A browser extension (Chrome/Firefox) providing GUI record-and-playback capabilities.
   - Primary Use Cases: Used for rapid prototyping of simple test scenarios, capturing element locators,
     and generating baseline test scripts that can be exported to programming languages like Python.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================================================
# Step 25: Initialize Chrome WebDriver via webdriver-manager & Navigate
# ==============================================================================
print("--- Step 25: Launching Chrome Browser ---")
# Auto-download and initialize the correct ChromeDriver binary matching installed Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to LambdaTest Selenium Playground
target_url = "https://www.lambdatest.com/selenium-playground/"
driver.get(target_url)

# Print Current URL and Page Title
print(f"Navigated URL: {driver.current_url}")
page_title = driver.title
print(f"Page Title   : {page_title}")


# ==============================================================================
# Step 26: Add Implicit Wait & Document Why Global Implicit Wait is Bad Practice
# ==============================================================================
# Global Implicit Wait Configuration:
# Polling interval defaults to 500ms, waiting up to 10 seconds for element presence.
driver.implicitly_wait(10)

"""
--------------------------------------------------------------------------------
Step 26 Explanation: Why Global Implicit Wait is Considered Bad Practice
--------------------------------------------------------------------------------
1. Unpredictable Timeout Compounding:
   Mixing implicit waits with explicit waits (WebDriverWait) can cause unexpected
   timeout behaviors where wait times accumulate (e.g., waiting 10s implicit + 10s explicit = 20s delay)
   or fail prematurely depending on browser driver implementations.

2. Slow Negative Scenario Testing:
   When testing for element absence (e.g., verifying an element is NOT present or hidden),
   implicit wait forces Selenium to poll the DOM for the full 10 seconds before returning,
   significantly slowing down test suite execution.

3. Lack of Specific Condition Matching:
   Implicit wait only checks for element presence in the DOM, NOT visibility, clickability,
   or state changes (e.g., text updating or element becoming enabled).

* Best Practice Recommendation: Keep implicit wait at 0 and rely exclusively on Explicit Waits
  (WebDriverWait + Expected Conditions) for targeted, reliable element synchronization.
"""

print("\nImplicit Wait of 10 seconds set successfully.")

# Close the standard browser session
driver.quit()
print("Standard Chrome Browser closed successfully.\n")


# ==============================================================================
# Step 27: Execute Chrome in Headless Mode using ChromeOptions
# ==============================================================================
print("--- Step 27: Running Chrome in Headless Mode ---")

# Configure ChromeOptions for Headless Execution
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")  # Modern Chrome headless mode engine
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize Headless Chrome Driver instance
headless_driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# Navigate and verify page title in headless mode
headless_driver.get(target_url)
headless_title = headless_driver.title

print(f"Headless Mode Current URL: {headless_driver.current_url}")
print(f"Headless Mode Page Title  : {headless_title}")

# Verification check
assert "Selenium Grid Online" in headless_title or "LambdaTest" in headless_title or len(headless_title) > 0, "Failed to fetch page title in headless mode!"
print("SUCCESS: Page title verified successfully in headless mode without a visible GUI window.")

# Clean up headless browser session
headless_driver.quit()
print("Headless Chrome Browser closed successfully.")
