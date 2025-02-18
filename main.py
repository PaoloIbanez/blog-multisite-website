# Most of the code commented out are code that was from the previous version, but wanted to keep to remember why I changed it and differences

from flask import Flask, render_template, request, redirect, url_for
import smtplib
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")  # Your email
PASSWORD = os.getenv("PASSWORD")  # Your email app password
# In main.py (or wherever you prefer)
BLOG_API_URL = "https://api.npoint.io/674f5423f73deab1e9a7"  # your real endpoint
response = requests.get(BLOG_API_URL)
all_posts = response.json()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        send_email(name, email, phone, message)

        return redirect(url_for("contact", success=True))  # Redirect to avoid resubmission

    return render_template("contact.html", success=request.args.get("success"))

def send_email(name, email, phone, message):
    subject = "New Contact Form Submission"
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(
            EMAIL,  # Sender
            EMAIL,  # Receiver (your own email)
            f"Subject: {subject}\n\n{body}"
        )


# @app.route('/contact')
# def contact():
#     return render_template("contact.html")

# @app.route('/post')
# def post():
#     return render_template("post.html")

@app.route('/post/<int:blog_id>')
def show_post(blog_id):
    """
    Renders the detail page for a single blog post with the given blog_id.
    Assumes you have a global 'all_posts' list, each post dict has an 'id'.
    """
    # Find the post with matching 'id' in all_posts
    requested_post = None
    for post in all_posts:
        if post["id"] == blog_id:
            requested_post = post
            break

    # Alternatively, a shorter approach:
    # requested_post = next((p for p in all_posts if p["id"] == blog_id), None)

    # Pass the matched post to post.html for rendering
    return render_template("post.html", post=requested_post)




if __name__ == "__main__":
    app.run(debug=True)
