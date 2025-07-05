from test_links import test_broken_links

print("[DEBUG] Script started")

url = "https://wikipedia.org"  # Replace with any site to test
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
except Exception as e:
    print("❌ Exception occurred:", str(e))
