"""
Browser Automation Script using Selenium
Automates clicks and edits on web pages.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time


class BrowserAutomation:
    def __init__(self, headless: bool = False):
        """Initialize Chrome browser with Selenium."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
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
    
    def type_text(self, selector: str, text: str, clear_first: bool = True, by: By = By.CSS_SELECTOR):
        """Type text into an input field."""
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        if clear_first:
            element.clear()
        element.send_keys(text)
        print(f"Typed '{text}' into: {selector}")
    
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
    
    def close(self):
        """Close the browser."""
        self.driver.quit()
        print("Browser closed")


# Example usage
if __name__ == "__main__":
    # Initialize browser
    browser = BrowserAutomation(headless=False)
    
    try:
        # Navigate to the website
        browser.go_to("https://iss.pg.com/paid-search-autobidder")
        
        # Wait a bit for the page to load
        time.sleep(3)
        
        # === ADD YOUR AUTOMATION STEPS HERE ===
        # Examples:
        # browser.click("#submit-button")
        # browser.click_by_text("Login")
        # browser.type_text("#username", "your_username")
        # browser.type_text("#password", "your_password")
        # browser.click("button[type='submit']")
        # browser.select_dropdown("#dropdown-id", "Option 1")
        
        # Keep browser open for manual inspection
        input("Press Enter to close the browser...")
        
    finally:
        browser.close()
