from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def test_page_load_time(url, driver_path):
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        start_time = time.time()
        driver.get(url)
        time.sleep(2) 
        load_time = (time.time() - start_time) * 1000  # ms

        return {
            "tested_url": url,
            "load_time_ms": round(load_time, 2)
        }

    except Exception as e:
        return {
            "tested_url": url,
            "load_time_ms": "unknown",
            "error": "❌ Could not load this page. Check if the URL is valid and online."
                }


    finally:
        if driver:
            driver.quit()
