from flask import Flask, render_template, redirect, send_file, url_for, request, session, make_response
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime
import markdown

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

'''
# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'curran.john35@gmail.com'

mail = Mail(app)
'''

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
    return render_template('home.html', projects=projects, working_on=working_on, theme=theme)


@app.route('/research-and-projects')
def research_and_projects():
    theme = session.get('theme', 'light')
    return render_template('research_and_projects.html', projects=projects, title="Research and Projects - John Curran", theme=theme)


projects = [
    {
        "id": 5,
        "title": "Delivery App Simulation",
        "description": "Modeling a delivery app using Python and sqlite.",
        "detail_url": "/projects/delivery_app_simulation",
        "github_url": "https://github.com/curohn/delivery_app_simulation",
        "tools": ["Python", "SQLite"],
        "markdown_file": "projects/delivery_app_simulation.md",
        "image":"",
        "date": "In Progress"
    }, 
    {
        "id": 4,
        "title": "Layoffs & Earnings Project",
        "description": "Are earnings a predictor of layoffs?",
        "detail_url": "/projects/layoffs_and_earnings",
        "github_url": "",
        "tools": [],
        "markdown_file": "projects/layoffs_and_earnings.md",
        "image":"",
        "date": "On Pause"
    },
    {
        "id": 3,
        "title": "Wage Distribution Analysis",
        "description": "Project to compare distributions in wages, over time",
        "detail_url": "/projects/wage_distribution",
        "github_url": "https://github.com/curohn/wage_distribution",
        "tools": ["Python", "Pandas", "Seaborn", "MatPlotLib"],
        "markdown_file": "projects/wage_distribution.md",
        "image":"",
        "date": "In Progress"
    },
    {
        "id": 2,
        "title": "Personal Website",
        "description": "Build a space to showcase my work and research, and develop some basic web development skills.",
        "detail_url": "/projects/personal_website",
        "github_url": "https://github.com/curohn/personal_blog",
        "tools": ["Python", "Flask", "CSS", "HTML", "Render"],
        "markdown_file": "projects/personal_website.md",
        "image":"",
        "date": "2024-12-11"
    },
    {
        "id": 1,
        "title": "Global Temperatures Analysis",
        "description": "A time series analysis of global surface temperatures. Used to demonstrate experience with linear regression in python.",
        "detail_url": "/projects/global_temperature_analysis",
        "github_url": "https://github.com/curohn/global_temperatures/tree/main",
        "tools": ["Python", "Pandas", "MatPlotLib", "scikit-learn"],
        "markdown_file": "projects/global_temperature_analysis.md",
        #"image": "images/global_temp_graph.png",
        "date": "2024-10-13"
    },
    
    # Add more projects as needed
]
working_on = [
    {
        "task": "Delivery App Simulation",
        "progress": 5,
        "project_name": "delivery_app_simulation"
    },
    {
        "task": "Wage Distribution Analysis",
        "progress": 50,
        "project_name": "wage_distribution"
    }
]

# Route to render project details
@app.route('/projects/<string:project_name>')
def project_detail(project_name):
    theme = session.get('theme', 'light')
    project = next((p for p in projects if p["detail_url"] == f"/projects/{project_name}"), None)
    if not project:
        return "Project not found", 404

    markdown_path = os.path.join(os.getcwd(), project.get("markdown_file"))
    if not os.path.exists(markdown_path):
        return "Writeup not found", 404

    with open(markdown_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    project_writeup = markdown.markdown(markdown_content)

    return render_template(
        'project_detail.html',
        project=project,
        writeup=project_writeup,
        projects=projects,
        theme=theme
    )



@app.route('/experience-and-education')
def experience_and_education():
    theme = session.get('theme', 'light')
    return render_template('experience_and_education.html', work_experience=work_experience, title="Experience and Education - John Curran", theme=theme)

work_experience = [
    {
        "title": "Senior Data Analyst",
        "company": "First American Title",
        "duration": "August 2023 – January 2025",
        "description": "Enhanced data accuracy and accessibility using Python and SQL, and developed dashboards for actionable insights."
    },
    {
        "title": "Senior Data Analyst",
        "company": "Ware2Go",
        "duration": "April 2022 – August 2023",
        "description": "Streamlined operations with automated notifications, identified $400k in missed billing, and ensured data integrity across projects."
    },
    {
        "title": "Data Analyst",
        "company": "Ware2Go",
        "duration": "April 2021 – March 2022",
        "description": "Revamped dashboards and created metrics for operations, boosting productivity and throughput analysis."
    },
    {
        "title": "Solutions Analyst Team Lead",
        "company": "APCO",
        "duration": "September 2019 – March 2021",
        "description": "Designed dashboards and reports using PowerBI and SQL, enabling improved decision-making during the Covid-19 pandemic."
    },
    {
        "title": "Solutions Analyst",
        "company": "APCO",
        "duration": "July 2018 – September 2019",
        "description": "Resolved technical issues and improved reporting workflows with SQL and Python."
    },
    {
        "title": "Education",
        "company": "East China Normal University",
        "duration": "August 2017 – February 2018",
        "description": "Chinese Language Program – Intensive Mandarin Chinese language course"
    },
    {
        "title": "Education",
        "company": "Florida State University",
        "duration": "August 2014 – May 2018",
        "description": "Bachelor of Science in International Affairs, with concentration in Economics. Activities: Vice President Florida State Rowing Team."
    }
]



'''
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    theme = session.get('theme', 'light')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Send email
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            sender=email,
            recipients=[recipient_email], 
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )

        mail.send(msg)
        return render_template('thank_you.html')  # Render the thank you page

    return render_template('contact.html', theme=theme)
'''

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
