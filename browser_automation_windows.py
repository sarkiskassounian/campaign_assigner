"""
Browser Automation Script - Windows Native Chrome
Connects to your existing Chrome browser via remote debugging.

SETUP (Windows):
1. Close all Chrome windows
2. Open Command Prompt and run:
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
3. Then run this script

For .exe packaging: pip install pyinstaller && pyinstaller --onefile browser_automation_windows.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class BrowserAutomation:
    def __init__(self, debug_port: int = 9222, use_existing_browser: bool = True):
        """
        Initialize Chrome browser connection.
        
        Args:
            debug_port: Port for Chrome remote debugging (default 9222)
            use_existing_browser: If True, connects to existing Chrome instance.
                                  If False, launches a new Chrome window.
        """
        chrome_options = Options()
        
        if use_existing_browser:
            # Connect to existing Chrome instance with remote debugging
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{debug_port}")
        else:
            # Launch new Chrome window (uses system Chrome)
            chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        print("Connected to Chrome browser")
    
    def go_to(self, url: str):
        """Navigate to a URL."""
        self.driver.get(url)
        print(f"Navigated to: {url}")
    
    def click(self, selector: str, by: By = By.CSS_SELECTOR):
        """Click an element by selector."""
        element = self.wait.until(EC.element_to_be_clickable((by, selector)))
        element.click()
        print(f"Clicked: {selector}")
    
    def click_by_text(self, text: str):
        """Click an element containing specific text."""
        xpath = f"//*[contains(text(), '{text}')]"
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print(f"Clicked element with text: {text}")
    
    def click_by_id(self, element_id: str):
        """Click an element by ID."""
        element = self.wait.until(EC.element_to_be_clickable((By.ID, element_id)))
        element.click()
        print(f"Clicked element with ID: {element_id}")
    
    def type_text(self, selector: str, text: str, clear_first: bool = True, by: By = By.CSS_SELECTOR):
        """Type text into an input field."""
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        if clear_first:
            element.clear()
        element.send_keys(text)
        print(f"Typed '{text}' into: {selector}")
    
    def type_by_id(self, element_id: str, text: str, clear_first: bool = True):
        """Type text into an input field by ID."""
        self.type_text(element_id, text, clear_first, by=By.ID)
    
    def select_dropdown(self, selector: str, value: str, by: By = By.CSS_SELECTOR):
        """Select an option from a dropdown by visible text."""
        from selenium.webdriver.support.ui import Select
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        select = Select(element)
        select.select_by_visible_text(value)
        print(f"Selected '{value}' from: {selector}")
    
    def wait_for_element(self, selector: str, timeout: int = 10, by: By = By.CSS_SELECTOR):
        """Wait for an element to be present."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, selector)))
    
    def get_text(self, selector: str, by: By = By.CSS_SELECTOR) -> str:
        """Get text from an element."""
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        return element.text
    
    def scroll_to_element(self, selector: str, by: By = By.CSS_SELECTOR):
        """Scroll to an element."""
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """Take a screenshot of the current page."""
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.driver.title
    
    def pause(self, seconds: float):
        """Pause execution."""
        time.sleep(seconds)
    
    def close(self):
        """Disconnect from browser (does NOT close the browser window)."""
        self.driver.quit()
        print("Disconnected from browser")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("IMPORTANT: Before running this script:")
    print("1. Close all Chrome windows")
    print("2. Open Command Prompt (cmd) and run:")
    print('   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
    print("3. Then run this script")
    print("=" * 60)
    
    input("Press Enter when Chrome is running with remote debugging...")
    
    # Connect to existing Chrome browser
    browser = BrowserAutomation(use_existing_browser=True)
    
    try:
        # Navigate to the website
        browser.go_to("https://iss.pg.com/paid-search-autobidder")
        
        # Wait for page to load
        browser.pause(3)
        
        # === ADD YOUR AUTOMATION STEPS HERE ===
        # Examples:
        # browser.click_by_id("submit-button")
        # browser.click_by_text("Login")
        # browser.type_by_id("username", "your_username")
        # browser.type_by_id("password", "your_password")
        # browser.click("button[type='submit']")
        
        print(f"Current URL: {browser.get_current_url()}")
        print(f"Page title: {browser.get_page_title()}")
        
        input("Press Enter to disconnect (browser stays open)...")
        
    finally:
        browser.close()
