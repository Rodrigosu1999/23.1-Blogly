from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users Model."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False,)
    last_name = db.Column(db.String(30),
                          nullable=False,)
    image_url = db.Column(db.String,
                          server_default='https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg')

    def get_full_name(self):
        """Get user full name."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Posts Model."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(30),
                      nullable=False,)
    content = db.Column(db.String(150),
                        nullable=False,)
    created_at = db.Column(db.DateTime)
    users_id = db.Column(db.Integer,
                         db.ForeignKey('users.id', ondelete='CASCADE'),
                         nullable=False
                         )

    user = db.relationship('User', backref=db.backref(
        'posts', passive_deletes=True))
