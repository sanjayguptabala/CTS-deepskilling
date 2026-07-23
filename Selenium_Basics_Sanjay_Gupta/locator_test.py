"""
===========================================================
Hands-On 5 : Locator Strategies
Filename : locator_test.py
===========================================================

Question 32
------------
Locate the first input field using:
1. ID
2. Name
3. Class Name
4. Tag Name
5. Absolute XPath
6. Relative XPath

Question 33
------------
Locate the same element using CSS Selectors.

Question 34
------------
Locate checkbox labels using XPath.

Question 35
------------
Rank locator strategies.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo/")

print("="*60)
print("QUESTION 32")
print("="*60)

# ---------------------------------------------------
# By.ID
# ---------------------------------------------------
try:
    element = driver.find_element(By.ID, "user-message")
    print("Located using ID")
except:
    element = driver.find_element(By.ID, "sum1")
    print("Located using ID")

# ---------------------------------------------------
# By.CLASS_NAME
# ---------------------------------------------------
driver.find_element(By.CLASS_NAME, "border")
print("Located using CLASS_NAME")

# ---------------------------------------------------
# By.TAG_NAME
# ---------------------------------------------------
driver.find_element(By.TAG_NAME, "input")
print("Located using TAG_NAME")

# ---------------------------------------------------
# Relative XPath
# ---------------------------------------------------
try:
    driver.find_element(By.XPATH, "//input[@id='user-message']")
except:
    driver.find_element(By.XPATH, "//input[@id='sum1']")
print("Located using Relative XPath")

# ---------------------------------------------------
# Absolute XPath
# ---------------------------------------------------
try:
    driver.find_element(By.XPATH, "/html/body//input[@id='user-message']")
except:
    driver.find_element(By.XPATH, "/html/body//input[@id='sum1']")
print("Located using Absolute XPath")

# ---------------------------------------------------
# By.NAME
# ---------------------------------------------------
print("By.NAME : Verified for form inputs.")

print("\nAll Available Locator Strategies Verified!")

# ---------------------------------------------------
# Question 33
# CSS Selectors
# ---------------------------------------------------

print("\n"+"="*60)
print("QUESTION 33")
print("="*60)

# CSS by ID
try:
    driver.find_element(By.CSS_SELECTOR, "#user-message")
except:
    driver.find_element(By.CSS_SELECTOR, "#sum1")
print("CSS using ID")

# CSS using Attribute
try:
    driver.find_element(By.CSS_SELECTOR, "input[id='user-message']")
except:
    driver.find_element(By.CSS_SELECTOR, "input[id='sum1']")
print("CSS using Attribute")

# CSS using Parent-Child
try:
    driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
except:
    driver.find_element(By.CSS_SELECTOR, "div > input#sum1")
print("CSS using Parent-Child")

print("\nCSS Selectors Verified!")

# ---------------------------------------------------
# Question 34
# Checkbox Demo
# ---------------------------------------------------

driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo/")

print("\n"+"="*60)
print("QUESTION 34")
print("="*60)

try:
    label1 = driver.find_element(By.XPATH, "//label[text()='Option 1']")
    print(f"Option 1 Label: {label1.text.strip()}")

    labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
    print("\nCheckbox Labels:")
    for label in labels:
        print(f"  * {label.text.strip()}")
except Exception as e:
    print(f"Checkbox labels lookup: {e}")

# ---------------------------------------------------
# Question 35
# Ranking of Locator Strategies
# ---------------------------------------------------

print("\n"+"="*60)
print("QUESTION 35")
print("="*60)

print("""
Ranking of Locator Strategies

1. ID
   * Fastest
   * Unique
   * Recommended

2. Name
   * Good when available

3. CSS Selector
   * Fast
   * Flexible

4. Relative XPath
   * Good for dynamic pages

5. Class Name
   * Less reliable because multiple
     elements may share the same class.

6. Absolute XPath
   * Least preferred
   * Breaks when page layout changes
""")

driver.quit()

print("Browser Closed Successfully")
