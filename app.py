"""Blogly application."""
from datetime import datetime
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()


# Homepage

@app.route("/")
def home():
    """Render 5 most recent posts"""
    posts = Post.query.order_by(db.desc(Post.created_at)).limit(5).all()
    return render_template("homepage.html", posts=posts)


# User's routes

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
    """Render create user form"""
    return render_template("user_create_form.html")


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


# Post's routes


@app.route("/users/<int:user_id>/posts/new")
def create_new_post(user_id):
    """Redirect to a the 'create post' page for the user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("create_post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_new_post_post_request(user_id):
    """Add new post for the user"""

    user = User.query.get_or_404(user_id)

    p_title = request.form['title']
    p_content = request.form['content']
    p_users_id = user.id
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=p_title, content=p_content,
                created_at=datetime.now(), users_id=p_users_id,
                user=user,
                tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def view_post(post_id):
    """Render the post"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("view_post.html",  post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Render the post edit form"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html",  post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_post_request(post_id):
    """Return the edited post"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post end redirect to  homepage"""

    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()

    return redirect("/")


# Tag's routes


@app.route("/tags")
def tags_list():
    """Render tags list"""
    tags = Tag.query.all()
    return render_template("tags_list.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_posts(tag_id):
    """Show posts related to a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_details.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Render edit tag form"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_post_request(tag_id):
    """Edit tag"""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")


@app.route("/tags/new")
def create_tag():
    """Render the create tag form"""

    return render_template("create_tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tag_post_request():
    """Add new tag to the database"""

    tag_name = request.form['name']

    tag = Tag(name=tag_name)

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag and redirect to tags list"""

    Tag.query.filter(Tag.id == tag_id).delete()

    db.session.commit()

    return redirect("/tags")


# 404 Route

@app.errorhandler(404)
def page_not_found(e):
    """Render html when we get 404 error"""
    return render_template('404.html'), 404
