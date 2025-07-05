from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def test_ui_elements(url, driver_path):
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(2) 

        results = {
            "tested_url": url,
            "nav_present": bool(driver.find_elements(By.TAG_NAME, "nav")),
            "footer_present": bool(driver.find_elements(By.TAG_NAME, "footer")),
            "button_present": bool(driver.find_elements(By.TAG_NAME, "button")),
            "form_present": bool(driver.find_elements(By.TAG_NAME, "form"))
        }

        return results

    except Exception as e:
        return {
            "tested_url": url,
            "error": "❌ Could not load this page. Check if the URL is valid and online."

        }

    finally:
        if driver:
            driver.quit()
