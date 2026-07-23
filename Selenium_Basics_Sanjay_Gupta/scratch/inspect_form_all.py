from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.testmuai.com/selenium-playground/input-form-demo/")

form = driver.find_element(By.ID, "seleniumform")
all_elems = form.find_elements(By.XPATH, ".//*")
for idx, elem in enumerate(all_elems):
    tag = elem.tag_name
    if tag in ["input", "select", "button", "textarea", "label"]:
        print(f"{idx}: tag='{tag}', id='{elem.get_attribute('id')}', name='{elem.get_attribute('name')}', text='{elem.text}', placeholder='{elem.get_attribute('placeholder')}'")

driver.quit()
