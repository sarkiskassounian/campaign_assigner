"""
Browser Automation Script using Playwright
Automates clicks and edits on web pages.
"""

from playwright.sync_api import sync_playwright, Page, Browser
import time


class BrowserAutomation:
    def __init__(self, headless: bool = False, ignore_https_errors: bool = True):
        """Initialize Chromium browser with Playwright."""
        self.playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(ignore_https_errors=ignore_https_errors)
        self.page: Page = self.context.new_page()
        self.page.set_default_timeout(10000)  # 10 seconds
    
    def go_to(self, url: str):
        """Navigate to a URL."""
        self.page.goto(url)
        print(f"Navigated to: {url}")
    
    def click(self, selector: str):
        """Click an element by CSS selector."""
        self.page.click(selector)
        print(f"Clicked: {selector}")
    
    def click_by_text(self, text: str):
        """Click an element containing specific text."""
        self.page.click(f"text={text}")
        print(f"Clicked element with text: {text}")
    
    def click_by_role(self, role: str, name: str = None):
        """Click an element by its role (button, link, etc.)."""
        if name:
            self.page.get_by_role(role, name=name).click()
            print(f"Clicked {role} with name: {name}")
        else:
            self.page.get_by_role(role).first.click()
            print(f"Clicked first {role}")
    
    def type_text(self, selector: str, text: str, clear_first: bool = True):
        """Type text into an input field."""
        if clear_first:
            self.page.fill(selector, text)
        else:
            self.page.type(selector, text)
        print(f"Typed '{text}' into: {selector}")
    
    def select_dropdown(self, selector: str, value: str):
        """Select an option from a dropdown by value or label."""
        self.page.select_option(selector, label=value)
        print(f"Selected '{value}' from: {selector}")
    
    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for an element to be present."""
        self.page.wait_for_selector(selector, timeout=timeout)
        print(f"Element found: {selector}")
    
    def wait_for_load(self):
        """Wait for page to finish loading."""
        self.page.wait_for_load_state("networkidle")
        print("Page fully loaded")
    
    def get_text(self, selector: str) -> str:
        """Get text from an element."""
        return self.page.inner_text(selector)
    
    def get_all_elements(self, selector: str) -> list:
        """Get all elements matching a selector."""
        return self.page.query_selector_all(selector)
    
    def scroll_to_element(self, selector: str):
        """Scroll to an element."""
        self.page.locator(selector).scroll_into_view_if_needed()
        print(f"Scrolled to: {selector}")
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """Take a screenshot of the current page."""
        self.page.screenshot(path=filename)
        print(f"Screenshot saved: {filename}")
    
    def pause(self, seconds: float):
        """Pause execution for a specified time."""
        time.sleep(seconds)
    
    def close(self):
        """Close the browser."""
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        print("Browser closed")


# Example usage
if __name__ == "__main__":
    # Initialize browser (set headless=True to run without GUI)
    browser = BrowserAutomation(headless=False)
    
    try:
        # Navigate to the website
        browser.go_to("https://iss.pg.com/paid-search-autobidder")
        
        # Wait for page to load
        browser.pause(3)
        
        # === ADD YOUR AUTOMATION STEPS HERE ===
        # Examples:
        # browser.click("#submit-button")
        # browser.click_by_text("Login")
        # browser.click_by_role("button", name="Submit")
        # browser.type_text("#username", "your_username")
        # browser.type_text("#password", "your_password")
        # browser.select_dropdown("#dropdown-id", "Option 1")
        # browser.take_screenshot("page.png")
        
        # Keep browser open for manual inspection
        input("Press Enter to close the browser...")
        
    finally:
        browser.close()
