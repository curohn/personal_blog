#!/usr/bin/env python3
"""
Local development script to sync project files.
Run this manually when you want to update project content.
"""

import os
import subprocess
import shutil
import stat
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

# Configuration
PROJECT_REPOS = {
    'delivery_app_simulation': 'https://github.com/curohn/delivery_app_simulation.git',
    'wage_distribution': 'https://github.com/curohn/wage_distribution.git', 
    'global_temperatures': 'https://github.com/curohn/global_temperatures.git',
    'georgia_power': 'https://github.com/curohn/georgia_power.git',
    'personal_blog': 'https://github.com/curohn/personal_blog.git'
}

def add_sync_metadata(content, repo_url, project_name):
    """Add metadata header to synced content."""
    header = f"""<!-- 
Auto-synced from: {repo_url}
Project: {project_name}
Last synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-->

"""
    return header + content

def clone_and_sync():
    """Clone repos temporarily and copy README files."""
    
    base_dir = Path(__file__).parent.parent
    projects_dir = base_dir / 'projects'
    temp_dir = base_dir / 'temp_repos'
    
    # Create temp directory
    temp_dir.mkdir(exist_ok=True)
    
    synced_count = 0
    
    try:
        for project_name, repo_url in PROJECT_REPOS.items():
            print(f"Syncing {project_name}...")
            
            # Clone repo to temp directory
            repo_dir = temp_dir / project_name
            if repo_dir.exists():
                safe_rmtree(repo_dir)
            
            try:
                result = subprocess.run(['git', 'clone', repo_url, str(repo_dir)], 
                                     check=True, capture_output=True, text=True)
                
                # Copy README.md to projects folder
                readme_path = repo_dir / 'README.md'
                if readme_path.exists():
                    target_name = project_name
                    if project_name == 'global_temperatures':
                        target_name = 'global_temperature_analysis'
                    
                    target_path = projects_dir / f'{target_name}.md'
                    
                    # Read content and add metadata
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add metadata and write to target
                    enhanced_content = add_sync_metadata(content, repo_url, project_name)
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(enhanced_content)
                    
                    print(f"✓ Copied README.md to {target_path.name}")
                    synced_count += 1
                else:
                    print(f"✗ No README.md found in {project_name}")
                    
            except subprocess.CalledProcessError as e:
                print(f"✗ Error cloning {project_name}: {e.stderr.decode() if e.stderr else str(e)}")
            except Exception as e:
                print(f"✗ Error processing {project_name}: {str(e)}")
    
    finally:
        # Clean up temp directory
        if temp_dir.exists():
            safe_rmtree(temp_dir)
    
    print(f"\nSync complete! Successfully synced {synced_count} projects.")
    if synced_count > 0:
        print("Your website will now show the latest content from your project repositories.")

if __name__ == "__main__":
    clone_and_sync()
