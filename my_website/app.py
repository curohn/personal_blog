from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

# Create a Flask application instance
app = Flask(__name__)

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
