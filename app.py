"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()


@app.route("/")
def home():
    return redirect("/users")


@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/new")
def create_user_form():
    users = User.query.all()
    return render_template("user_create_form.html", users=users)


@app.route("/users/new", methods=["POST"])
def create_user_post_request():
    """Add pet and redirect to list."""

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
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_post_request(user_id):
    """Add pet and redirect to list."""

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
    """Show info on a single pet."""

    User.query.filter(User.id == user_id).delete()

    db.session.commit()

    return redirect("/")
