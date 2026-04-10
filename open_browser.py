import webbrowser

url = "https://iss.pg.com/paid-search-autobidder"

# Try to open in Chrome specifically
try:
    chrome = webbrowser.get("google-chrome")
    chrome.open(url)
except webbrowser.Error:
    # Fallback to chromium or default browser
    try:
        chrome = webbrowser.get("chromium")
        chrome.open(url)
    except webbrowser.Error:
        webbrowser.open(url)
