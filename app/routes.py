from flask import Blueprint, render_template, request
from tests.test_performance import test_page_load_time
from tests.test_ui import test_ui_elements
from utils.crawler import crawl_site
from utils.link_checker import check_links_multithreaded
from datetime import datetime

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html", year=datetime.now().year)

@main.route("/run-test", methods=["POST"])
def run_test():
    url = request.form.get("url")

    # Normalize URL
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    if "w3schools.com" in url and "www." not in url:
        url = url.replace("https://", "https://www.")

    # Deep test checkbox
    run_deep = request.form.get("run_deep_tests") == "on"

    driver_path = r"C:\Users\SHREYA\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    # Crawl and limit to 30 pages
    all_pages = list(crawl_site(url, max_depth=1))
    all_pages = all_pages[:30]

    # Multithreaded check with 20 workers
    link_results = check_links_multithreaded(all_pages, max_threads=20)

    # Filter out JS stub links
    link_results = [link for link in link_results if not link['url'].startswith("javascript:")]

    broken_links = [l for l in link_results if l["is_broken"]]
    valid_links = [l for l in link_results if not l["is_broken"]]

    results = {
        "tested_url": url,
        "total_links": len(link_results),
        "valid_links": len(valid_links),
        "broken_links": len(broken_links),
        "broken_list": broken_links
    }

    # Only test homepage with Selenium if deep scan is ON
    if run_deep:
        try:
            load_result = test_page_load_time(url, driver_path)
        except Exception as e:
            load_result = {"error": f"❌ Could not load this page. Check if the URL is valid and online."}
        try:
            ui_result = test_ui_elements(url, driver_path)
        except Exception as e:
            ui_result = {"error": f"❌ Could not load this page. Check if the URL is valid and online."}
    else:
        load_result = {"skipped": True}
        ui_result = {"skipped": True}

    return render_template("result.html", results=results, load_result=load_result, ui_result=ui_result)
