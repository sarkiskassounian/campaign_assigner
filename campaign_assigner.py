"""
Campaign Assigner - Standalone Windows Application
Self-contained automation tool that works without Python installation.

This script:
1. Automatically launches Chrome with remote debugging
2. Connects to Chrome and performs automation
3. All bundled into a single .exe with PyInstaller
"""

import subprocess
import time
import sys
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def find_chrome_path():
    """Find Chrome installation path on Windows."""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def launch_chrome_with_debugging(port: int = 9222):
    """Launch Chrome with remote debugging enabled."""
    chrome_path = find_chrome_path()
    
    if not chrome_path:
        print("ERROR: Chrome not found. Please install Google Chrome.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"Found Chrome at: {chrome_path}")
    print(f"Launching Chrome with remote debugging on port {port}...")
    
    # Launch Chrome with remote debugging
    # Using a separate user data dir to avoid conflicts with existing Chrome
    user_data_dir = os.path.join(os.environ.get('TEMP', '.'), 'chrome_automation_profile')
    
    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    
    # Launch Chrome as a separate process (non-blocking)
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for Chrome to start
    print("Waiting for Chrome to start...")
    time.sleep(3)
    
    return True


def connect_to_chrome(port: int = 9222, max_retries: int = 5):
    """Connect to Chrome via remote debugging."""
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"localhost:{port}")
    
    for attempt in range(max_retries):
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print("Successfully connected to Chrome!")
            return driver
        except WebDriverException as e:
            if attempt < max_retries - 1:
                print(f"Connecting... (attempt {attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"Failed to connect to Chrome: {e}")
                return None
    
    return None


class BrowserAutomation:
    def __init__(self, driver):
        """Initialize with an existing WebDriver connection."""
        self.driver = driver
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


def run_automation(browser: BrowserAutomation):
    """
    Main automation logic - customize this function!
    Add your clicks, typing, and other automation steps here.
    """
    # Navigate to the target website
    browser.go_to("https://iss.pg.com/paid-search-autobidder")
    
    # Wait for page to load
    browser.pause(3)
    
    print(f"\nCurrent URL: {browser.get_current_url()}")
    print(f"Page title: {browser.get_page_title()}")
    
    # ============================================
    # ADD YOUR AUTOMATION STEPS HERE
    # ============================================
    # Examples:
    # browser.click_by_id("login-button")
    # browser.type_by_id("username", "your_username")
    # browser.type_by_id("password", "your_password")
    # browser.click_by_text("Submit")
    # browser.select_dropdown("#campaign-dropdown", "Campaign 1")
    # browser.click("button.save-btn")
    # ============================================
    
    print("\n✓ Automation completed successfully!")


def main():
    print("=" * 60)
    print("  Campaign Assigner - Browser Automation Tool")
    print("=" * 60)
    print()
    
    DEBUG_PORT = 9222
    
    # Step 1: Launch Chrome with debugging
    launch_chrome_with_debugging(DEBUG_PORT)
    
    # Step 2: Connect to Chrome
    driver = connect_to_chrome(DEBUG_PORT)
    
    if not driver:
        print("\nFailed to connect to Chrome.")
        print("Please make sure no other Chrome instances are running and try again.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 3: Run automation
    browser = BrowserAutomation(driver)
    
    try:
        run_automation(browser)
        
        print("\n" + "=" * 60)
        print("Browser will remain open for you to continue working.")
        print("Close this window when done.")
        print("=" * 60)
        input("\nPress Enter to exit...")
        
    except Exception as e:
        print(f"\nError during automation: {e}")
        input("Press Enter to exit...")
    
    finally:
        # Disconnect (but don't close the browser)
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    main()
