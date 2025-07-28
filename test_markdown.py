#!/usr/bin/env python3
"""
Test script to verify markdown loading works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils import load_project_markdown

def test_markdown_loading():
    """Test loading markdown content for projects."""
    projects_to_test = [
        'delivery_app_simulation',
        'wage_distribution', 
        'global_temperature_analysis'
    ]
    
    for project in projects_to_test:
        print(f"\n=== Testing {project} ===")
        content = load_project_markdown(project)
        
        if content:
            print(f"✓ Successfully loaded content ({len(content)} characters)")
            # Show first few lines
            lines = content.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"Preview: {line[:80]}...")
                    break
        else:
            print(f"✗ Failed to load content")

if __name__ == "__main__":
    test_markdown_loading()
