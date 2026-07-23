from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.testmuai.com/selenium-playground/checkbox-demo/")

checkbox = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")[0]
print(f"Initial selected: {checkbox.is_selected()}")
checkbox.click()
print(f"Selected after click: {checkbox.is_selected()}")
checkbox.click()
print(f"Selected after second click: {checkbox.is_selected()}")

driver.quit()
