import requests
from concurrent.futures import ThreadPoolExecutor

def check_link(url):
    if not isinstance(url, str):
        return {"url": str(url), "status": "invalid", "is_broken": True}

    # Ignore JS, tel:, mailto:
    if url.startswith(("javascript:", "tel:", "mailto:")):
        return {
            "url": url,
            "status": "ignored",
            "is_broken": False
        }
    try:
        response = requests.get(url, timeout=5)
        return {
            "url": url,
            "status": response.status_code,
            "is_broken": response.status_code >= 400
        }
    except Exception:
        return {
            "url": url,
            "status": "error",
            "is_broken": True
        }

def check_links_multithreaded(url_list, max_threads=10):
    with ThreadPoolExecutor(max_threads) as executor:
        results = list(executor.map(check_link, url_list))
    return results
