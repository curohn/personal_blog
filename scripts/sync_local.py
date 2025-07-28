#!/usr/bin/env python3
"""
Local development script to sync project files.
Run this manually when you want to update project content.
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

def download_image(image_url, local_path):
    """Download an image from URL to local path."""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"  ✗ Image not found at URL: {image_url}")
            print(f"    Check if the image exists in the repository and is committed to main branch")
        else:
            print(f"  ✗ HTTP error downloading image: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Failed to download image: {e}")
        return False

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

def find_image_in_repo(repo_dir, image_filename):
    """Find an image file in the repository, checking common directories."""
    common_paths = [
        image_filename,  # Root directory
        f"images/{image_filename}",
        f"assets/{image_filename}",
        f"img/{image_filename}",
        f"static/{image_filename}",
        f"docs/{image_filename}"
    ]
    
    for path in common_paths:
        full_path = repo_dir / path
        if full_path.exists():
            return path
    
    # Search recursively if not found in common paths
    for file_path in repo_dir.rglob(image_filename):
        if file_path.is_file():
            return str(file_path.relative_to(repo_dir)).replace('\\', '/')
    
    return None
    """Find an image file in the repository, checking common directories."""
    common_paths = [
        image_filename,  # Root directory
        f"images/{image_filename}",
        f"assets/{image_filename}",
        f"img/{image_filename}",
        f"static/{image_filename}",
        f"docs/{image_filename}"
    ]
    
    for path in common_paths:
        full_path = repo_dir / path
        if full_path.exists():
            return path
    
    # Search recursively if not found in common paths
    for file_path in repo_dir.rglob(image_filename):
        if file_path.is_file():
            return str(file_path.relative_to(repo_dir)).replace('\\', '/')
    
    return None

def process_images_in_markdown(content, repo_name, project_name, base_dir, repo_dir):
    """Download images referenced in markdown and update paths."""
    # Find all image references in markdown
    image_pattern = r'!\[([^\]]*)\]\(([^)]+\.(png|jpg|jpeg|gif|svg))\)'
    images_found = re.findall(image_pattern, content)
    
    if not images_found:
        return content
    
    print(f"  Found {len(images_found)} images to sync...")
    
    # Get the default branch for this repository
    default_branch = get_default_branch(repo_dir)
    print(f"  Using branch: {default_branch}")
    
    # Create project-specific image directory
    images_dir = base_dir / 'static' / 'images' / 'projects' / project_name
    images_dir.mkdir(parents=True, exist_ok=True)
    
    updated_content = content
    
    for alt_text, image_path, extension in images_found:
        # Skip if it's already a full URL
        if image_path.startswith(('http://', 'https://')):
            continue
            
        # Extract just the filename
        image_filename = os.path.basename(image_path)
        
        # First, try to find the image in the local repo
        actual_image_path = find_image_in_repo(repo_dir, image_filename)
        
        if actual_image_path:
            # Use the actual path found in the repo
            github_image_url = f"https://raw.githubusercontent.com/{repo_name}/{default_branch}/{actual_image_path}"
            print(f"  Found image at: {actual_image_path}")
        else:
            # Fall back to the original path from markdown
            github_image_url = f"https://raw.githubusercontent.com/{repo_name}/{default_branch}/{image_path}"
            print(f"  Trying original path: {image_path}")
        
        # Local path for the image
        local_image_path = images_dir / image_filename
        
        # Download the image
        if download_image(github_image_url, local_image_path):
            # Update the markdown to use the static path
            new_path = f"/static/images/projects/{project_name}/{image_filename}"
            old_markdown = f'![{alt_text}]({image_path})'
            new_markdown = f'![{alt_text}]({new_path})'
            updated_content = updated_content.replace(old_markdown, new_markdown)
            print(f"  ✓ Downloaded and updated: {image_filename}")
        else:
            print(f"  ✗ Failed to download: {image_filename}")
            # List available image files for debugging
            image_files = list(repo_dir.rglob(f"*.{extension}"))
            if image_files:
                print(f"  Available {extension} files in repo:")
                for img_file in image_files[:5]:  # Show first 5
                    rel_path = img_file.relative_to(repo_dir)
                    print(f"    - {rel_path}")
    
    return updated_content

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
                print(f"  Cloned successfully")
                
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
                    
                    # Extract repo name from URL (e.g., "curohn/delivery_app_simulation")  
                    repo_name = repo_url.replace('https://github.com/', '').replace('.git', '')
                    
                    # Process images and update paths
                    content = process_images_in_markdown(content, repo_name, project_name, base_dir, repo_dir)
                    
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
        print("\nTo view your updated website:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Navigate to your project pages to see the synced content and images!")

if __name__ == "__main__":
    clone_and_sync()
