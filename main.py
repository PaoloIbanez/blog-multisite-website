from flask import Flask, render_template
import requests

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

@app.route('/contact')
def contact():
    return render_template("contact.html")

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
