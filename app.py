"""Blogly application."""
from datetime import datetime
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()


@app.route("/")
def home():
    posts = Post.query.limit(5).all()
    return render_template("homepage.html", posts=posts)


@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.users_id == user_id)
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/new")
def create_user_form():
    users = User.query.all()
    return render_template("user_create_form.html", users=users)


@app.route("/users/new", methods=["POST"])
def create_user_post_request():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show info on a single user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_post_request(user_id):
    """Add user and redirect to list."""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.image_url = user.image_url if request.form['image_url'] else "https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg"

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user end redirect to the root route"""

    user = User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect("/")


@app.route("/users/<int:user_id>/posts/new")
def create_new_post(user_id):
    """Redirect to a the 'create post' page for the user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.users_id == user_id)
    return render_template("create_post.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_new_post_post_request(user_id):
    """Add new post for the user"""

    user = User.query.get_or_404(user_id)

    p_title = request.form['title']
    p_content = request.form['content']
    p_users_id = user.id

    post = Post(title=p_title, content=p_content,
                created_at=datetime.now(), users_id=p_users_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def view_post(post_id):
    """Render the post"""

    post = Post.query.get_or_404(post_id)
    return render_template("view_post.html",  post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Render the post"""

    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html",  post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_post_request(post_id):
    """Add new post for the user"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post end redirect to  homepage"""

    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()

    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    """Render html when we get 404 error"""
    return render_template('404.html'), 404
