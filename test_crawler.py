from utils.crawler import crawl_site

urls = crawl_site("https://python.org", max_depth=1)
print(f"Total internal pages found: {len(urls)}")
for url in urls:
    print(url)
