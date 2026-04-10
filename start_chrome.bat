@echo off
echo Starting Chrome with remote debugging on port 9222...
echo.
echo After Chrome opens, run campaign_assigner.exe to automate.
echo.
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
