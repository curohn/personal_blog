#!/usr/bin/env pwsh
Write-Host "Syncing project files from GitHub repositories..." -ForegroundColor Green
Write-Host ""

# Change to the script's parent directory
Set-Location (Split-Path $PSScriptRoot -Parent)

# Run the sync script
python scripts\sync_local.py

Write-Host ""
Write-Host "Sync complete! You can now run your Flask app to see the updated content." -ForegroundColor Green
Write-Host "To start the app: python app.py" -ForegroundColor Yellow
