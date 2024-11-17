from flask import Flask, render_template, request


# Create a Flask application instance
app = Flask(__name__)

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
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Message received from {name} ({email}): {message}")
        return "Thank you for your message!"
    return render_template('contact.html')


# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
