import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_internal_link(link, base_domain):
    try:
        parsed_link = urlparse(link)
        return (parsed_link.netloc == '' or parsed_link.netloc == base_domain)
    except:
        return False

def crawl_site(start_url, max_depth=2):
    visited = set()
    to_visit = [(start_url, 0)]
    all_links = set()

    base_domain = urlparse(start_url).netloc

    while to_visit:
        current_url, depth = to_visit.pop()
        if current_url in visited or depth > max_depth:
            continue

        visited.add(current_url)
        all_links.add(current_url)

        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            a_tags = soup.find_all("a")

            for tag in a_tags:
                href = tag.get("href")
                if not href:
                    continue

                full_url = urljoin(current_url, href)
                if is_internal_link(full_url, base_domain) and full_url not in visited:
                    to_visit.append((full_url, depth + 1))
        except Exception as e:
            print(f"[WARN] Could not crawl {current_url}: {e}")

    return all_links
