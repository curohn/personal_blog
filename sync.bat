@echo off
echo Syncing project files from GitHub repositories...
echo.

cd /d "%~dp0.."
python scripts\sync_local.py

echo.
echo Sync complete! You can now run your Flask app to see the updated content.
echo To start the app: python app.py
pause
