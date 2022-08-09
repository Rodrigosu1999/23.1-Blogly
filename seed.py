"""Seed file to make sample data for db."""
from datetime import datetime
from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Make a lot of users
u1 = User(first_name="Yiyo", last_name="Serrano")
u2 = User(first_name="Erika", last_name="Andrade")
u3 = User(first_name="Franco", last_name="Escamilla")
u4 = User(first_name="Bob", last_name="Marley")


db.session.add_all([u1, u2, u3, u4])

db.session.commit()

# # Make a bunch of posts


p1 = Post(title="First Post", content="Hello everyone, this is my first post!",
          created_at=datetime.now(), users_id=1)
p2 = Post(title="My First Post", content="Hello everyone, I'm Erika!",
          created_at=datetime.now(), users_id=2)
p3 = Post(title="Hello", content="Hello all the way from mars!",
          created_at=datetime.now(), users_id=3)
p4 = Post(title="Second Post", content="Im getting the hang of this",
          created_at=datetime.now(), users_id=1)
p5 = Post(title="Why?", content="Why are we here?",
          created_at=datetime.now(), users_id=4)
p6 = Post(title="Help the other guy", content="He's writing weird stuff",
          created_at=datetime.now(), users_id=2)


db.session.add_all([p1, p2, p3, p4, p5, p6])

db.session.commit()
