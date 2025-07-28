#!/usr/bin/env python3
"""
Sync project files from GitHub repositories to local projects folder.
"""

import requests
import os
import sys
from urllib.parse import urlparse

# Project configuration - maps project names to their GitHub repos
PROJECTS = {
    'delivery_app_simulation': {
        'repo': 'curohn/delivery_app_simulation',
        'files': ['README.md'],  # Files to sync from the repo
        'target': 'delivery_app_simulation.md'
    },
    'wage_distribution': {
        'repo': 'curohn/wage_distribution', 
        'files': ['README.md'],
        'target': 'wage_distribution.md'
    },
    'global_temperature_analysis': {
        'repo': 'curohn/global_temperatures',
        'files': ['README.md'],
        'target': 'global_temperature_analysis.md'
    },
    # Add more projects as needed
}

def fetch_file_content(repo, file_path, branch='main'):
    """Fetch file content from GitHub repository."""
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{file_path}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {file_path} from {repo}: {e}")
        return None

def sync_project_files():
    """Sync project files from GitHub repositories."""
    projects_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'projects')
    
    # Ensure projects directory exists
    os.makedirs(projects_dir, exist_ok=True)
    
    for project_name, config in PROJECTS.items():
        print(f"Syncing {project_name}...")
        
        repo = config['repo']
        target_file = config['target']
        
        # For now, just sync the first file (usually README.md)
        # Could be extended to combine multiple files
        source_file = config['files'][0]
        
        content = fetch_file_content(repo, source_file)
        
        if content:
            target_path = os.path.join(projects_dir, target_file)
            
            # Add metadata header
            header = f"""---
# Auto-synced from: https://github.com/{repo}
# Source file: {source_file}
# Last synced: {__import__('datetime').datetime.now().isoformat()}
---

"""
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(header + content)
            
            print(f"✓ Synced {target_file}")
        else:
            print(f"✗ Failed to sync {target_file}")

if __name__ == "__main__":
    sync_project_files()
    print("Sync complete!")
