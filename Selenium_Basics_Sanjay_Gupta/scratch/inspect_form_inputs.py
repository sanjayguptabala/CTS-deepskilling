from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.testmuai.com/selenium-playground/input-form-demo/")

print("=== INPUTS INSIDE FORM ===")
form = driver.find_element(By.ID, "seleniumform")
for idx, inp in enumerate(form.find_elements(By.TAG_NAME, "input")):
    print(f"{idx}: tag='{inp.tag_name}', id='{inp.get_attribute('id')}', name='{inp.get_attribute('name')}', placeholder='{inp.get_attribute('placeholder')}'")

driver.quit()
