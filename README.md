# Campaign Assigner

Browser automation tool for the Paid Search Autobidder. Creates a standalone Windows `.exe` that works without Python installed.

## What It Does

- Automatically launches Chrome with remote debugging
- Connects to your Chrome browser (uses your existing logins/cookies)
- Performs automated clicks, typing, and form submissions
- Bundles Python runtime - **no Python installation required for end users**

## For Developers (Building the .exe)

### Prerequisites
- Windows PC with Python 3.8+ installed
- Google Chrome installed

### Build Steps

1. Clone this repository
2. Run the build script:
   ```cmd
   build.bat
   ```
3. Find the executable at: `dist\CampaignAssigner.exe`

### Alternative build with spec file:
```cmd
pip install selenium pyinstaller
pyinstaller campaign_assigner.spec
```

## For End Users (Running the .exe)

### Prerequisites  
- Google Chrome installed
- **No Python needed!**

### How to Use

1. **Close all Chrome windows** (important!)
2. Double-click `CampaignAssigner.exe`
3. Chrome will open automatically
4. The automation will run

## Customizing the Automation

Edit the `run_automation()` function in `campaign_assigner.py`:

```python
def run_automation(browser: BrowserAutomation):
    browser.go_to("https://iss.pg.com/paid-search-autobidder")
    browser.pause(3)
    
    # Add your steps here:
    browser.click_by_id("login-button")
    browser.type_by_id("username", "your_username")
    browser.type_by_id("password", "your_password")
    browser.click_by_text("Submit")
    browser.select_dropdown("#campaign", "Campaign Name")
```

### Available Methods

| Method | Description |
|--------|-------------|
| `go_to(url)` | Navigate to a URL |
| `click(selector)` | Click element by CSS selector |
| `click_by_id(id)` | Click element by ID |
| `click_by_text(text)` | Click element containing text |
| `type_text(selector, text)` | Type into input field |
| `type_by_id(id, text)` | Type into input by ID |
| `select_dropdown(selector, value)` | Select dropdown option |
| `wait_for_element(selector)` | Wait for element to appear |
| `get_text(selector)` | Get text from element |
| `scroll_to_element(selector)` | Scroll to element |
| `take_screenshot(filename)` | Save screenshot |
| `pause(seconds)` | Wait for specified time |

## Files

| File | Purpose |
|------|---------|
| `campaign_assigner.py` | Main automation script |
| `build.bat` | Builds the .exe |
| `campaign_assigner.spec` | PyInstaller configuration |
| `requirements.txt` | Python dependencies |

## Troubleshooting

**"Chrome not found"**  
Install Google Chrome from https://google.com/chrome

**"Failed to connect to Chrome"**  
Close all Chrome windows and try again

**Element not found errors**  
Increase wait times with `browser.pause(5)` or check your selectors