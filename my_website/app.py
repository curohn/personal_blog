from flask import Flask, render_template, send_file, url_for, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime

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
    print("Home route accessed")
    return render_template('home.html')  # Render the home page template

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects)
projects = [
    {
        "id": 1,
        "title": "Global Temperatures Analysis",
        "description": "A time series analysis of global surface temperatures. Used to demonstrate experience with linear regression in python.",
        "image": "sales_dashboard.png",
        "detail_url": "/projects/global-temperature-analysis",
        "github_url": "https://github.com/curohn/global_temperatures/tree/main",
        "methodology": """- Import dataset using Pandas 
            - Clean data, Add features like averages, remove inaccurate data, etc. 
            - Calcuate upper and lower uncertainty bounds
            - Fit the linear regression model to the data using scikit-learn
            - Plot the data using MatPlotLib
        """,
        "graphs": [""],
        "tools": ["Python", "Pandas", "MatPlotLib", "scikit-learn"],
        "date": "2024-03-31"

    },
    {
        "id": 2,
        "title": "PLACEHOLDER: Customer Segmentation",
        "description": "Clustering customer data to uncover distinct buying behaviors.",
        "image": "customer_segmentation.png",
        "detail_url": "/projects/customer-segmentation",
        "github_url": "",
        "methodology": """PLACEHOLDER: 
            - Performed exploratory data analysis to find customer patterns.
            - Applied K-Means clustering to group customers by purchasing habits.
            - Visualized clusters with Matplotlib and Seaborn.
        """,
        "graphs": ["clusters.png"],
        "tools": [],
        "date": "2024-03-31"
    },
    # Add more projects as needed
]



@app.route('/projects/<string:project_name>')
def project_detail(project_name):
    project = next((p for p in projects if p["detail_url"] == f"/projects/{project_name}"), None)
    if not project:
        return "Project not found", 404
    
    # Format the date
    project['formatted_date'] = datetime.strptime(project['date'], "%Y-%m-%d").strftime("%B %d, %Y")
    return render_template('project_detail.html', project=project, projects=projects)




@app.route('/resume')
def resume():
    return render_template('resume.html')  # Render the resume page template

@app.route('/blog')
def blog():
    posts = [
        {"title": "My First Blog Post", "content": "This is my first post!", "date": "2024-01-01"},
        {"title": "Learning Flask", "content": "Flask is a great framework for web development.", "date": "2024-01-15"},
    ]
    return render_template('blog.html', posts=posts)


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




# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
