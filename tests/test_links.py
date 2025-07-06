import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

MAX_LINKS_TO_CHECK = 20  # Limit the number of links checked per test

def get_link_error_details(status_code, url):
    """Get detailed information about a broken link error"""
    error_info = {
        "severity": "medium",
        "description": "",
        "suggestions": [],
        "category": "unknown"
    }
    
    if status_code == 404:
        error_info.update({
            "severity": "high",
            "description": "Page not found - The requested page doesn't exist on the server",
            "suggestions": [
                "Check if the URL is correct and the page hasn't been moved",
                "Update the link to point to the correct page",
                "Consider setting up a redirect if the page has been moved",
                "Remove the link if the content is no longer available"
            ],
            "category": "not_found"
        })
    elif status_code == 403:
        error_info.update({
            "severity": "medium",
            "description": "Forbidden - Access to this resource is denied",
            "suggestions": [
                "Check if the page requires authentication",
                "Verify if the link should be publicly accessible",
                "Contact the website administrator if this is unexpected",
                "Consider removing the link if it's not meant to be public"
            ],
            "category": "access_denied"
        })
    elif status_code == 500:
        error_info.update({
            "severity": "medium",
            "description": "Internal Server Error - The server encountered an error",
            "suggestions": [
                "This is likely a temporary server issue",
                "Try accessing the link later",
                "Contact the website administrator if the problem persists",
                "Consider removing the link if it's consistently broken"
            ],
            "category": "server_error"
        })
    elif status_code == 502:
        error_info.update({
            "severity": "medium",
            "description": "Bad Gateway - The server received an invalid response",
            "suggestions": [
                "This is usually a temporary issue",
                "Try accessing the link later",
                "The target server might be down or overloaded",
                "Consider checking the link periodically"
            ],
            "category": "server_error"
        })
    elif status_code == 503:
        error_info.update({
            "severity": "low",
            "description": "Service Unavailable - The server is temporarily unavailable",
            "suggestions": [
                "This is a temporary maintenance issue",
                "Try accessing the link later",
                "The service should be restored soon",
                "No action needed unless the issue persists"
            ],
            "category": "maintenance"
        })
    elif status_code == 301 or status_code == 302:
        error_info.update({
            "severity": "low",
            "description": f"Redirect ({status_code}) - The page has been moved",
            "suggestions": [
                "Update the link to point to the new URL",
                "The redirect should work automatically",
                "Consider updating your bookmarks or references",
                "This is usually not a critical issue"
            ],
            "category": "redirect"
        })
    elif status_code == 400:
        error_info.update({
            "severity": "medium",
            "description": "Bad Request - The server cannot process the request",
            "suggestions": [
                "Check if the URL format is correct",
                "Verify that all required parameters are included",
                "The link might be malformed",
                "Contact the website administrator if needed"
            ],
            "category": "client_error"
        })
    elif status_code == 401:
        error_info.update({
            "severity": "medium",
            "description": "Unauthorized - Authentication is required",
            "suggestions": [
                "This page requires login credentials",
                "Check if the link should be publicly accessible",
                "Consider if this link is appropriate for your audience",
                "Remove the link if it's not meant to be public"
            ],
            "category": "authentication"
        })
    elif status_code == 408:
        error_info.update({
            "severity": "medium",
            "description": "Request Timeout - The server took too long to respond",
            "suggestions": [
                "This might be a temporary network issue",
                "Try accessing the link later",
                "The server might be overloaded",
                "Consider if the link is still relevant"
            ],
            "category": "timeout"
        })
    elif status_code == 429:
        error_info.update({
            "severity": "low",
            "description": "Too Many Requests - Rate limit exceeded",
            "suggestions": [
                "This is a temporary rate limiting issue",
                "Try accessing the link later",
                "The server is protecting against abuse",
                "No immediate action needed"
            ],
            "category": "rate_limit"
        })
    elif status_code == "error":
        error_info.update({
            "severity": "high",
            "description": "Connection Error - Unable to reach the server",
            "suggestions": [
                "Check if the URL is correct",
                "Verify that the website is still online",
                "The domain might have expired or been moved",
                "Consider removing the link if the site is gone"
            ],
            "category": "connection"
        })
    else:
        error_info.update({
            "severity": "medium",
            "description": f"HTTP {status_code} - Unknown error occurred",
            "suggestions": [
                "Check the specific HTTP status code meaning",
                "Try accessing the link manually to understand the issue",
                "Contact the website administrator if needed",
                "Consider removing the link if it's consistently broken"
            ],
            "category": "unknown"
        })
    
    return error_info

def test_broken_links(url, driver_path=None):
    # Use the local Windows path for ChromeDriver by default
    if driver_path is None:
        driver_path = "C:/Users/SHREYA/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(2)
    
    anchors = driver.find_elements(By.TAG_NAME, "a")
    links = [a.get_attribute("href") for a in anchors if a.get_attribute("href")]
    driver.quit()

    # Limit the number of links checked
    links = links[:MAX_LINKS_TO_CHECK]

    results = []
    for link in links:
        # Skip None or empty links
        if not link:
            continue
            
        try:
            if link.startswith("mailto:") or link.startswith("javascript:") or link.startswith("tel:"):
                error_details = get_link_error_details("error", link)
                results.append({
                    "url": link, 
                    "status": "error", 
                    "is_broken": True,
                    "error_details": error_details
                })
                continue

            res = requests.head(link, allow_redirects=True, timeout=5)
            status = res.status_code
            is_broken = status >= 400
            
            if is_broken:
                error_details = get_link_error_details(status, link)
                results.append({
                    "url": link, 
                    "status": status, 
                    "is_broken": True,
                    "error_details": error_details
                })
            else:
                results.append({
                    "url": link, 
                    "status": status, 
                    "is_broken": False
                })
                
        except Exception as e:
            if 'ERR_NAME_NOT_RESOLVED' in str(e):
                return {"error": "❌ Could not resolve the website address. Please check the URL and try again."}
            status = "error"
            is_broken = True
            error_details = get_link_error_details(status, link)
            results.append({
                "url": link, 
                "status": status, 
                "is_broken": True,
                "error_details": error_details
            })

    valid_links = [r for r in results if not r["is_broken"]]
    broken_links = [r for r in results if r["is_broken"]]

    return {
        "tested_url": url,
        "total_links": len(results),
        "valid_links": len(valid_links),
        "broken_links": len(broken_links),
        "broken_list": broken_links
    }