from flask import Flask, render_template, send_file, url_for, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime
import markdown

load_dotenv()

# Create a Flask application instance
app = Flask(__name__)

# Track downloads
@app.route('/download_resume')
@app.route('/download_resume')
def download_resume():
    resume_path = os.path.join(app.static_folder, 'curran_john_resume.pdf')

    # Log the download to a file
    with open("downloads.log", "a") as log:
        log.write(f"Resume downloaded at {datetime.now()}\n")

    # Serve the PDF file for download
    return send_file(resume_path, as_attachment=True, download_name="curran_john_resume.pdf")


# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'curran.john35@gmail.com'

mail = Mail(app)


# Define routes for different pages
@app.route('/')
def home():
    return render_template('home.html', projects=projects, working_on=working_on)


@app.route('/work-and-research')
def work_and_research_page():
    return render_template(
        'projects.html', 
        projects=projects, 
        title="Work and Research - John Curran",
        description="Explore my portfolio of work and research, featuring data analysis projects and personal explorations."
    )

projects = [
    {
        "id": 1,
        "title": "Global Temperatures Analysis",
        "description": "A time series analysis of global surface temperatures. Used to demonstrate experience with linear regression in python.",
        "detail_url": "/projects/global_temperature_analysis",
        "github_url": "https://github.com/curohn/global_temperatures/tree/main",
        "tools": ["Python", "Pandas", "MatPlotLib", "scikit-learn"],
        "markdown_file": "projects/global_temperature_analysis.md",
        "date": "2024-10-13"

    },
    {
        "id": 2,
        "title": "Personal Website",
        "description": "Build a space to showcase my work and research, and develop some basic web development skills.",
        "detail_url": "/projects/personal_website",
        "github_url": "https://github.com/curohn/personal_blog",
        "tools": ["Python", "Flask", "CSS", "HTML"],
        "markdown_file": "projects/personal_website.md",
        "date": "Working On"
    },
    # Add more projects as needed
]
working_on = [
    {
        "task": "Building a Personal Website",
        "progress": 40,
        "project_name": "personal_website"
    }
]



# Route to render project details
@app.route('/projects/<string:project_name>')
def project_detail(project_name):
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
        projects=projects
    )



@app.route('/resume')
def resume():
    return render_template('resume.html')  # Render the resume page template


@app.route('/contact', methods=['GET', 'POST'])
def contact():
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

    return render_template('contact.html')

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
