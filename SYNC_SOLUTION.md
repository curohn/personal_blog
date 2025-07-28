# Project Sync Solution

This solution automatically syncs README files from your individual project repositories into your personal blog website.

## How It Works

1. **Individual Project Repos**: Each of your projects (delivery_app_simulation, wage_distribution, etc.) has its own GitHub repository with a README.md file.

2. **Sync Script**: The `scripts/sync_local.py` script clones each repository temporarily, extracts the README.md, and copies it to your website's `projects/` folder.

3. **Flask Integration**: Your Flask app (`app.py`) automatically detects markdown files and renders them using the `markdown_template.html` template, falling back to existing HTML templates if needed.

## Usage

### Option 1: Run Python Script Directly
```bash
python scripts/sync_local.py
```

### Option 2: Use Batch File (Windows)
```bash
sync.bat
```

### Option 3: Use PowerShell Script
```powershell
./sync.ps1
```

## What Gets Synced

The script currently syncs these repositories:
- `curohn/delivery_app_simulation` → `delivery_app_simulation.md`
- `curohn/wage_distribution` → `wage_distribution.md`  
- `curohn/global_temperatures` → `global_temperature_analysis.md`

## Adding New Projects

To add a new project to the sync:

1. Edit `scripts/sync_local.py`
2. Add your new repository to the `PROJECT_REPOS` dictionary:
   ```python
   PROJECT_REPOS = {
       'your_new_project': 'https://github.com/curohn/your_new_project.git',
       # ... existing projects
   }
   ```
3. Add the corresponding entry to your `projects` list in `app.py`

## Features

- ✅ **Single Source of Truth**: Maintain content only in your project repositories
- ✅ **Automatic Metadata**: Adds sync timestamps and source repository info
- ✅ **Windows Compatible**: Handles file permission issues on Windows
- ✅ **Error Handling**: Graceful handling of network issues or missing files  
- ✅ **Markdown to HTML**: Automatic conversion with syntax highlighting and tables
- ✅ **Progress Tracking**: Shows project progress bars from your `working_on` data
- ✅ **GitHub Integration**: Direct links to source repositories

## Workflow

1. **Update Project**: Make changes to your individual project repositories
2. **Sync Content**: Run `python scripts/sync_local.py` or `sync.bat`
3. **Deploy**: Your website now shows the latest content from your projects

## Automation Options

For full automation, you can:
- Set up the GitHub Actions workflow (`.github/workflows/sync-projects.yml`)
- Run the sync script as a cron job
- Trigger sync via webhook when you push to project repositories

## Files Structure

```
personal_blog/
├── scripts/
│   ├── sync_local.py          # Main sync script
│   ├── sync_projects.py       # GitHub Actions version
│   └── setup_submodules.sh    # Git submodule alternative
├── projects/                  # Synced markdown files
│   ├── delivery_app_simulation.md
│   ├── wage_distribution.md
│   └── global_temperature_analysis.md
├── templates/projects/
│   └── markdown_template.html # Generic template for markdown content
├── utils.py                   # Markdown processing utilities
├── sync.bat                   # Windows batch script
└── sync.ps1                   # PowerShell script
```

This solution keeps your project content in sync automatically while maintaining the professional look of your website!
