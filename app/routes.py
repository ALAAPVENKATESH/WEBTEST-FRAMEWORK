from flask import Blueprint, render_template, request, jsonify, session
from tests.test_links import test_broken_links
from tests.test_performance import test_page_load_time
from tests.test_ui import test_ui_elements
from tests.test_seo import test_seo_elements
from tests.test_security import test_security_elements
from tests.test_images import test_images
from datetime import datetime
import re
import json
import signal
import threading
import time

main = Blueprint('main', __name__)

@main.route("/")
def home():
    # Get test history from session
    test_history = session.get('test_history', [])
    return render_template("index.html", year=datetime.now().year, test_history=test_history)

@main.route("/run-test", methods=["POST"])
def run_test():
    url = request.form.get("url")
    if not url:
        return render_template(
            "result.html",
            results={"error": "❌ No URL provided. Please enter a website URL."},
            load_result={"error": "❌ No URL provided."},
            ui_result={"error": "❌ No URL provided."}
        )
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    driver_path = "C:/Users/SHREYA/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

    try:
        link_results = test_broken_links(url, driver_path)
        performance_results = test_page_load_time(url, driver_path)
        ui_results = test_ui_elements(url, driver_path)
        seo_results = test_seo_elements(url)
        security_results = test_security_elements(url)
        image_results = test_images(url)

        # If any test returns a dict with 'error', show a friendly error page
        for result in (link_results, performance_results, ui_results):
            if isinstance(result, dict) and result.get("error"):
                return render_template(
                    "result.html",
                    results=link_results,
                    load_result=performance_results,
                    ui_result=ui_results
                )

        # Calculate overall score
        overall_score = calculate_overall_score(
            link_results, performance_results, ui_results, seo_results, security_results, image_results
        )

        # Save test results to session history
        test_history = session.get('test_history', [])
        test_history.append({
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "link_results": link_results,
            "performance_results": performance_results,
            "ui_results": ui_results,
            "seo_results": seo_results,
            "security_results": security_results,
            "image_results": image_results,
            "overall_score": overall_score
        })
        session['test_history'] = test_history

        return render_template(
            "result.html",
            results=link_results,
            load_result=performance_results,
            ui_result=ui_results
        )

    except Exception as e:
        if 'ERR_NAME_NOT_RESOLVED' in str(e):
            return render_template(
                "result.html",
                results={"tested_url": url, "total_links": 0, "valid_links": 0, "broken_links": 0, "broken_list": [], "error": "❌ Could not resolve the website address. Please check the URL and try again."},
                load_result={"error": "❌ Could not resolve the website address. Please check the URL and try again."},
                ui_result={"error": "❌ Could not resolve the website address. Please check the URL and try again."}
            )
        return f"<h1>Error occurred</h1><pre>{str(e)}</pre>"

@main.route("/api/test", methods=["POST"])
def api_test():
    """API endpoint for programmatic testing"""
    data = request.get_json()
    url = data.get("url", "").strip()
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    driver_path = "C:/Users/SHREYA/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    
    try:
        results = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "link_test": test_broken_links(url, driver_path),
            "performance_test": test_page_load_time(url, driver_path),
            "ui_test": test_ui_elements(url, driver_path),
            "seo_test": test_seo_elements(url),
            "security_test": test_security_elements(url),
            "image_test": test_images(url)
        }
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/history")
def test_history():
    """Show test history page"""
    test_history = session.get('test_history', [])
    return render_template("history.html", test_history=test_history, year=datetime.now().year)

@main.route("/export/<int:test_index>")
def export_result(test_index):
    """Export test result as JSON"""
    test_history = session.get('test_history', [])
    if 0 <= test_index < len(test_history):
        return jsonify(test_history[test_index])
    return jsonify({"error": "Test not found"}), 404

@main.route("/broken-links-details")
def broken_links_details():
    """Show detailed broken links information"""
    # Get the latest test results from session
    test_history = session.get('test_history', [])
    if not test_history:
        return render_template("errors/500.html", custom_message="No test history found. Please run a test first."), 200
    
    latest_test = test_history[-1]
    if 'link_test' not in latest_test or 'broken_list' not in latest_test['link_test']:
        return render_template("errors/500.html", custom_message="No broken link details found for the latest test."), 200
    
    return render_template("broken_links_details.html", 
                         broken_links=latest_test['link_test']['broken_list'],
                         tested_url=latest_test['url'])

def calculate_overall_score(link_results, performance_results, ui_results, seo_results, security_results, image_results):
    """Calculate overall website score"""
    scores = []
    
    # Link score (0-100)
    if 'error' not in link_results:
        link_score = 100 - (link_results.get('broken_links', 0) * 10)
        scores.append(max(0, link_score))
    
    # Performance score (0-100)
    if 'load_time_ms' in performance_results:
        load_time = performance_results['load_time_ms']
        if load_time < 1000:
            perf_score = 100
        elif load_time < 3000:
            perf_score = 80
        elif load_time < 5000:
            perf_score = 60
        else:
            perf_score = 40
        scores.append(perf_score)
    
    # UI score (0-100)
    if 'error' not in ui_results:
        ui_elements = [ui_results.get('navbar', False), ui_results.get('footer', False), 
                      ui_results.get('button', False), ui_results.get('form', False)]
        ui_score = (sum(ui_elements) / len(ui_elements)) * 100
        scores.append(ui_score)
    
    # SEO score (0-100)
    if 'seo_score' in seo_results:
        seo_score = (seo_results['seo_score'] / 6) * 100
        scores.append(seo_score)
    
    # Security score (0-100)
    if 'security_score' in security_results:
        security_score = (security_results['security_score'] / 6) * 100
        scores.append(security_score)
    
    # Image score (0-100)
    if 'image_score' in image_results:
        image_score = (image_results['image_score'] / 3) * 100
        scores.append(image_score)
    
    if scores:
        overall = sum(scores) / len(scores)
        return round(overall, 1)
    return 0
