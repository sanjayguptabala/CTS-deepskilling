from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.testmuai.com/selenium-playground/checkbox-demo/")

checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
print(f"Total checkboxes: {len(checkboxes)}")
for idx, cb in enumerate(checkboxes):
    print(f"{idx}: id='{cb.get_attribute('id')}', name='{cb.get_attribute('name')}', displayed={cb.is_displayed()}, selected={cb.is_selected()}")

driver.quit()
