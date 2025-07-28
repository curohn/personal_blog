from flask import Flask, render_template, redirect, send_file, url_for, request, session, make_response
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime
import markdown
from utils import load_project_markdown

load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Track downloads
@app.route('/download_resume')
def download_resume():
    resume_path = os.path.join(app.static_folder, 'curran_john_resume.pdf')

    # Log the download to a file
    with open("downloads.log", "a") as log:
        log.write(f"Resume downloaded at {datetime.now()}\n")

    # Serve the PDF file for download
    return send_file(resume_path, as_attachment=True, download_name="curran_john_resume.pdf")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")


# Toggle Theme Route
@app.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    response = make_response(redirect(request.referrer or url_for('home')))
    return response


# Define routes for different pages
@app.route('/')
def home():
    theme = session.get('theme', 'light')
    featured_projects = [p for p in projects if p.get("featured", False)]  # Filter featured projects
    return render_template('home.html', projects=featured_projects, working_on=working_on, theme=theme)


@app.route('/research-and-projects')
def research_and_projects():
    theme = session.get('theme', 'light')
    return render_template('research_and_projects.html', projects=projects, title="Research and Projects - John Curran", theme=theme)


projects = [
    {
        "id": 7,
        "title": "Work",
        "description": "A write up of my current work.",
        "detail_url": "/projects/work",
        "github_url": "",
        "tools": ["Python", "SQL", "Airbyte", "Redshift", "Metabase", "dbt"],
        "date": "Ongoing"
    },
    {
        "id": 6,
        "title": "Delivery App Simulation",
        "description": "Modeling a delivery app using Python and sqlite.",
        "detail_url": "/projects/delivery_app_simulation",
        "github_url": "https://github.com/curohn/delivery_app_simulation",
        "tools": ["Python", "SQLite"],
        "date": "On Hold",
        "featured": True  # Added featured attribute
    },
    {
        "id": 5,
        "title": "Self Study",
        "description": "What I'm currently working on to improve my skills.",
        "detail_url": "/projects/self_study",
        "github_url": "",
        "tools": [],
        "date": "On Hold",
        "featured": False  # Added featured attribute
    },
    {
        "id": 4,
        "title": "Georgia Power",
        "description": "A project to analyze and visualize Georgia Power's data.",
        "detail_url": "/projects/georgia_power",
        "github_url": "https://github.com/curohn/georgia_power",
        "featured": True
    },
    {
        "id": 3,
        "title": "Wage Distribution Analysis",
        "description": "Project to compare distributions in wages, over time",
        "detail_url": "/projects/wage_distribution",
        "github_url": "https://github.com/curohn/wage_distribution",
        "tools": ["Python", "Pandas", "Seaborn", "MatPlotLib"],
        "date": "On Hold",
        "featured": True
    },
    {
        "id": 2,
        "title": "Personal Website",
        "description": "Build a space to showcase my work and research, and develop some basic web development skills.",
        "detail_url": "/projects/personal_website",
        "github_url": "https://github.com/curohn/personal_blog",
        "tools": ["Python", "Flask", "CSS", "HTML", "Render"],
        "date": "2024-12-11",
        "featured": True
    },
    {
        "id": 1,
        "title": "Global Temperatures Analysis",
        "description": "A time series analysis of global surface temperatures. Used to demonstrate experience with linear regression in python.",
        "detail_url": "/projects/global_temperature_analysis",
        "github_url": "https://github.com/curohn/global_temperatures/tree/main",
        "tools": ["Python", "Pandas", "MatPlotLib", "scikit-learn"],
        "date": "2024-10-13",
        "featured": True
    },
    
    # Add more projects as needed
]
working_on = [
    {
        "task": "Work",
        "progress": 100,
        "project_name": "work"
    },
    {
        "task": "Self Study",
        "progress": 0,
        "project_name": "self_study"
    },
    {
        "task": "Delivery App Simulation",
        "progress": 45,
        "project_name": "delivery_app_simulation"
    }
]
# Route to render project pages dynamically
@app.route('/projects/<string:project_name>')
def project_detail(project_name):
    theme = session.get('theme', 'light')
    project = next((p for p in projects if p["detail_url"] == f"/projects/{project_name}"), None)
    if not project:
        return "Project not found", 404

    # Try to load markdown content first
    markdown_content = load_project_markdown(project_name)
    
    if markdown_content:
        # Get progress from working_on list
        progress = None
        for item in working_on:
            if item.get("project_name") == project_name:
                progress = item.get("progress")
                break
        
        return render_template(
            'projects/markdown_template.html',
            theme=theme,
            projects=sorted(projects, key=lambda p: p["id"], reverse=True),
            current_project_id=project["id"],
            project=project,
            content=markdown_content,
            progress=progress
        )
    
    # Fallback to HTML template if no markdown found
    try:
        return render_template(
            f'projects/{project_name}.html',
            theme=theme,
            projects=sorted(projects, key=lambda p: p["id"], reverse=True),
            current_project_id=project["id"]
        )
    except:
        return "Project template not found", 404


@app.route('/experience-and-education')
def experience_and_education():
    theme = session.get('theme', 'light')
    return render_template('experience_and_education.html', work_experience=work_experience, title="Experience and Education - John Curran", theme=theme)

work_experience = [
    {
        "title": "Education",
        "company": "Georgia State University",
        "duration": "Fall 2025 - Spring 2027 (anticipated)",
        "description": (
            " - Pursuing a Masters in Data Science and Analytics at Georgia State University's J. Mack Robinson College of Business. <br> "
            " - Courses will include: Machine Learning, Predictive Analytics, Statistics, and Data communication."
        )
    },
    {
        "title": "Data & Reporting Manager",
        "company": "SmartPM",
        "duration": "May 2025 – Present",
        "description": (
            " - Developed and implemented a comprehensive data strategy, enhancing data-driven decision-making across the organization. <br>"
            " - Developed a data warehouse, etl processes, and a data viz/dashboarding system."
            "Leading the development of a new data warehouse and reporting system, enhancing data accessibility and reporting capabilities. <br>"
            " - Collaborating with cross-functional teams to define KPIs and develop reporting solutions. <br>"
            
        )
    },
    {
        "title": "Senior Data Analyst",
        "company": "First American Title",
        "duration": "August 2023 – January 2025",
        "description": (
            " - Led pilot programs to evaluate and enhance future initiatives, collaborating with cross-functional teams to define KPIs and develop reporting solutions. <br>"
            " - Designed and implemented data monitoring processes using Snowflake and Python, achieving 99%+ data integrity. <br>"
            " - Developed interactive dashboards for real-time insights, empowering stakeholders with actionable data. <br>"
            " - Spearheaded company-wide data strategy initiatives and translated complex analytics into clear business insights."
        )
    },
    {
        "title": "Senior Data Analyst",
        "company": "Ware2Go",
        "duration": "April 2022 – August 2023",
        "description": (
            " - Built an email notification system using Python, SQL, and Airflow, delivering relevant data to over 100 users. <br>"
            " - Established a correction bounty program, reducing operational issues by 10%. <br>"
            " - Led a billing audit project that uncovered $400k in annual missed revenue.<br> "
            " - Maintained department dashboards in DOMO and ensured data quality across 15+ projects, integrating APIs, tables, and ETL processes."
        )
    },
    {
        "title": "Data Analyst",
        "company": "Ware2Go",
        "duration": "April 2021 – March 2022",
        "description": (
            " - Revamped team dashboards, optimizing ETL processes to reduce reporting lag from 1 hour to 15 minutes. <br>"
            " - Created warehouse productivity and throughput metrics, driving operational improvements.<br> "
            " - Conducted deep-dive analyses into processes, delivering actionable insights for key optimizations."
        )
    },
    {
        "title": "Solutions Analyst Team Lead",
        "company": "APCO",
        "duration": "September 2019 – March 2021",
        "description": (
            " - Designed dashboards and reports using Excel, PowerBI, and SQL, delivering actionable insights in clear presentations. <br>"
            " - Developed an Excel dashboard to track daily receivables during the Covid-19 pandemic, enabling critical sales decisions. <br>"
            " - Reworked reports by adding new features, migrating data sources, and rewriting SQL scripts to enhance functionality."
        )
    },
    {
        "title": "Solutions Analyst",
        "company": "APCO",
        "duration": "July 2018 – September 2019",
        "description": (
            " - Investigated and resolved technical user issues, leveraging skills in Excel, SQL, and Python. <br>"
            " - Streamlined reporting workflows and improved data accessibility for stakeholders."
        )
    },
    {
        "title": "Education",
        "company": "East China Normal University",
        "duration": "August 2017 – February 2018",
        "description": " - Completed an intensive Mandarin Chinese language program."
    },
    {
        "title": "Education",
        "company": "Florida State University",
        "duration": "August 2014 – May 2018",
        "description": (
            " - Earned a Bachelor of Science in International Affairs with a concentration in Economics. <br>"
            " - Served as Vice President of the Florida State Rowing Team."
        )
    }
]


@app.route('/sitemap.xml')
def sitemap():
    from flask import Response
    import datetime

    pages = set()  # Use a set to avoid duplicates
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.add(rule.rule)

    sitemap_xml = render_template(
        'sitemap.xml',
        pages=[{
            "loc": f"{request.url_root.rstrip('/')}{page}",
            "lastmod": datetime.datetime.now().date()
        } for page in pages]
    )
    return Response(sitemap_xml, mimetype='application/xml')


# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
