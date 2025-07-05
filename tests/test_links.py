from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urljoin

def test_broken_links(url, driver_path):
    print("[DEBUG] Inside test_broken_links")

    # Set up ChromeDriver in headless mode
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)

    # Open the page
    try:
        driver.get(url)
    except Exception as e:
        driver.quit()
        return {
            "tested_url": url,
            "total_links": 0,
            "valid_links": 0,
            "broken_links": 0,
            "broken_list": [],
            "error": "❌ Could not load this page. Check if the URL is valid and online."

        }

    # Find all <a> tags
    anchor_tags = driver.find_elements(By.TAG_NAME, "a")
    all_links = []

    print(f"[DEBUG] Found {len(anchor_tags)} <a> tags")

    for tag in anchor_tags:
        href = tag.get_attribute("href")
        if href:
            full_url = urljoin(url, href)
            all_links.append(full_url)

    driver.quit()
    all_links = all_links[:20]

    print(f"[DEBUG] Collected {len(all_links)} links")

    broken_links = []
    valid_links = []

    for link in all_links:
        try:
            response = requests.head(link, allow_redirects=True, timeout=5)
            status = response.status_code
            if status >= 400:
                broken_links.append({"url": link, "status": status})
            else:
                valid_links.append(link)
        except requests.RequestException:
            broken_links.append({"url": link, "status": "Connection Error"})

    result = {
        "tested_url": url,
        "total_links": len(all_links),
        "valid_links": len(valid_links),
        "broken_links": len(broken_links),
        "broken_list": broken_links
    }

    print("[DEBUG] Returning result dictionary")
    return result
