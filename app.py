#Importing the required packages and modules for this app
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from jinja2 import TemplateNotFound
import os

app = Flask(__name__)

# This is the standard way to configure sqlite database with sqlalchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/blog/blog.db'

# This is the best way to configure sqlite database with sqlalchemy without bugs by splitting the full database path into 2 parts:
# First we create a variable file_path. We use os module to get the current working directory using getcwd() + the database file name
file_path = os.path.abspath(os.getcwd()) + "/mydb.db"

# Now after we created file_path variable that holds the full database file path, we just add sqlite:/// to it to initialize the configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path

# Now we create a database instance db for our app instance using SQLAlchemy that we imported
db = SQLAlchemy(app)

# Create a database table to store the data of blog posts
class MyBlogPost(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(40))
	post_description = db.Column(db.String(60))
	author = db.Column(db.String(40))
	post_date = db.Column(db.DateTime)
	body = db.Column(db.Text)

# Handling the page not found error (404 error) and returning the rendered 404.html page
# the error e wraps the function pageNotFound() by passing it in as a parameter
@app.errorhandler(404)
def pageNotFoundError(e):
    return render_template("404.html")

# Routing and rendering the home page
@app.route("/")
def home():
	posts = MyBlogPost.query.order_by(MyBlogPost.post_date.desc()).all()
	return render_template("index.html", posts = posts)

# Custom class for the about page
class AboutPage:
	def __init__(self, page=str):
		self.about = page

	def get_about(self):
		if self.about:
			return self.about

# Class instance for the about page
about_object = AboutPage("about.html")

# Routing and rendering the about page
@app.route("/about")
def about():
	return render_template(about_object.get_about())

# Routing and rendering dinamically the posts created by users
@app.route("/post/<int:post_id>")
def post(post_id):
	post = MyBlogPost.query.filter_by(id = post_id).one()
	return render_template("post.html", post = post)

# Routing and rendering create_post page
@app.route("/create_post")
def create_post():
	return render_template("create_post.html")


# Routing and rendering new_post page
@app.route("/new_post", methods = ["POST"])
def created():
	# Using a list to store user post data of the only database table we have for this app
	data_list = [request.form["title"], request.form["post_description"], request.form["author"], request.form["body"]]
	
	# Creating a variable for each element in the list using list indexing
	title = data_list[0]
	post_description = data_list[1]
	author = data_list[2]
	body = data_list[3]
	
	# Creating a n instance that representes th blog post created by a user
	post = MyBlogPost(title = title, post_description = post_description, author = author, body = body, post_date = datetime.now())

	# Add post to database
	db.session.add(post)
	# Commit post addition to database
	db.session.commit()

	# Redirecting the user to the home page after submission of their new post
	return redirect(url_for("home"))

# Making sure the app.py file runs only when it is executed from this file itself and not when it is imported
if __name__ == '__main__':
	app.run(debug = True)
