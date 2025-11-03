from playwright.sync_api import sync_playwright

def run_browser(base_url: str, headless: bool = True):
    """Optional: open the HotStreak website for JavaScript-rendered content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(base_url)
        print(f"Opened {base_url}")
        browser.close()
