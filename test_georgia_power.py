#!/usr/bin/env python3
"""
Test script to sync just georgia_power project to debug the branch issue.
"""

import os
import subprocess
import shutil
import stat
import re
import requests
from pathlib import Path
from datetime import datetime

def handle_remove_readonly(func, path, exc):
    """Error handler for Windows readonly files during rmtree."""
    if os.path.exists(path):
        os.chmod(path, stat.S_IWRITE)
        func(path)

def safe_rmtree(path):
    """Safely remove directory tree on Windows."""
    if path.exists():
        shutil.rmtree(path, onerror=handle_remove_readonly)

def get_default_branch(repo_dir):
    """Get the default branch name for a repository."""
    try:
        # Check what branch we're currently on
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              cwd=repo_dir, capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        
        if current_branch:
            return current_branch
            
        # Fallback: check remote default branch
        result = subprocess.run(['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'], 
                              cwd=repo_dir, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('/')[-1]
            
    except Exception:
        pass
    
    # Default fallbacks
    return 'main'

# Test just georgia_power
repo_url = 'https://github.com/curohn/georgia_power.git'
project_name = 'georgia_power'

base_dir = Path(__file__).parent.parent
temp_dir = base_dir / 'temp_repos'
temp_dir.mkdir(exist_ok=True)

try:
    repo_dir = temp_dir / project_name
    if repo_dir.exists():
        safe_rmtree(repo_dir)
    
    print(f"Cloning {project_name}...")
    result = subprocess.run(['git', 'clone', repo_url, str(repo_dir)], 
                         check=True, capture_output=True, text=True)
    
    print("Detecting branch...")
    branch = get_default_branch(repo_dir)
    print(f"Detected branch: {branch}")
    
    # Check for the image file
    image_filename = "ga_power_20250728.png"
    print(f"\nLooking for {image_filename}...")
    
    # List all PNG files
    png_files = list(repo_dir.rglob("*.png"))
    print(f"Found PNG files:")
    for png in png_files:
        rel_path = png.relative_to(repo_dir)
        print(f"  - {rel_path}")
    
    # Test the URL
    repo_name = repo_url.replace('https://github.com/', '').replace('.git', '')
    test_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/{image_filename}"
    print(f"\nTesting URL: {test_url}")
    
    response = requests.head(test_url)
    print(f"Response status: {response.status_code}")

finally:
    if temp_dir.exists():
        safe_rmtree(temp_dir)
