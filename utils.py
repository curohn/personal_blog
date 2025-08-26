import markdown
import os
import re
from datetime import datetime

def markdown_to_html(markdown_content):
    """Convert markdown content to HTML."""
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables', 
        'toc',
        'codehilite'
    ])
    return md.convert(markdown_content)

def load_project_markdown(project_name):
    """Load markdown content for a project."""
    projects_dir = os.path.join(os.path.dirname(__file__), 'projects')
    markdown_file = os.path.join(projects_dir, f'{project_name}.md')
    
    if os.path.exists(markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove HTML comments (metadata)
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL).strip()
        
        # Remove metadata header if present (YAML frontmatter)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        
        return markdown_to_html(content)
    
    return None