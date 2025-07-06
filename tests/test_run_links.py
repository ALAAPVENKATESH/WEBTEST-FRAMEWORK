from test_links import test_broken_links

print("[DEBUG] Script started")

url = input("Enter the website to test (e.g., wikipedia.org): ").strip()

if not url.startswith("http://") and not url.startswith("https://"):
    url = "https://" + url

driver_path = "C:/Users/SHREYA/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

try:
    results = test_broken_links(url, driver_path)
    print("[DEBUG] Function returned successfully")

    print("\n===== TEST RESULTS =====")
    print(f"Tested URL: {results['tested_url']}")
    print(f"Total Links: {results['total_links']}")
    print(f"Valid Links: {results['valid_links']}")
    print(f"Broken Links: {results['broken_links']}")
    print("\nBroken Link Details:")
    for item in results["broken_list"]:
        print(f" - {item['url']} → {item['status']}")
        if 'error_details' in item:
            print(f"   Severity: {item['error_details']['severity'].upper()}")
            print(f"   Category: {item['error_details']['category'].replace('_', ' ').title()}")
            print(f"   Description: {item['error_details']['description']}")
            print(f"   Suggestions:")
            for suggestion in item['error_details']['suggestions']:
                print(f"     • {suggestion}")
        print()
except Exception as e:
    print("❌ Exception occurred:", str(e))