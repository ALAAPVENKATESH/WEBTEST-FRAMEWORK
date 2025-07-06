from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def test_ui_elements(url, driver_path):
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    def element_exists(selectors):
        if isinstance(selectors, str):
            selectors = [selectors]
        for selector in selectors:
            if len(driver.find_elements(By.CSS_SELECTOR, selector)) > 0:
                return True
        return False

    try:
        # More comprehensive selectors for navigation
        navbar_selectors = [
            "nav", "header", "[role='navigation']", ".navbar", ".nav", ".navigation",
            ".header", ".main-nav", ".primary-nav", ".top-nav", ".menu",
            "#header", "#navbar", "#navigation", "#nav", ".topbar", ".toolbar"
        ]
        
        # More comprehensive selectors for footer
        footer_selectors = [
            "footer", "[role='contentinfo']", ".footer", ".site-footer", ".main-footer",
            ".bottom", ".bottom-nav", "#footer", ".footer-nav", ".footer-menu"
        ]
        
        # Button selectors
        button_selectors = [
            "button", "[role='button']", ".btn", ".button", "input[type='button']",
            "input[type='submit']", ".cta", ".action-button"
        ]
        
        # Form selectors
        form_selectors = [
            "form", ".form", ".search-form", ".contact-form", ".login-form",
            ".signup-form", ".newsletter-form"
        ]

        return {
            "navbar": element_exists(navbar_selectors),
            "footer": element_exists(footer_selectors),
            "button": element_exists(button_selectors),
            "form": element_exists(form_selectors)
        }
    except Exception as e:
        if 'ERR_NAME_NOT_RESOLVED' in str(e):
            return {"error": "❌ Could not resolve the website address. Please check the URL and try again."}
        return {"error": f"Selenium UI check failed. ({str(e).splitlines()[0]})"}
    finally:
        driver.quit()
