from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

# https://live-forex-signals.com/en/
driver = webdriver.Chrome()
driver.get('https://live-forex-signals.com/en/')
wait = WebDriverWait(driver, 10)
divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body')))
if divs:
    data = []
    for div in divs:
        if 'Filled' not in div.text and 'Premium' not in div.text:
            data.append(div.text.strip())

    print(data.__len__())
else:
    print("Không tìm thấy thẻ div với class 'card-body' trên trang.")