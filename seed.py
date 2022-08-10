"""Seed file to make sample data for db."""
from datetime import datetime
from models import User, Post, Tag, PostTag, db
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

# Make a bunch of posts


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

# Make some tags

t1 = Tag(name="Welcome")
t2 = Tag(name="Sad")
t3 = Tag(name="Worried")
t4 = Tag(name="Happy")

db.session.add_all([t1, t2, t3, t4])

db.session.commit()

# Make some Post-Tag relations!

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=4)
pt3 = PostTag(post_id=2, tag_id=1)
pt4 = PostTag(post_id=2, tag_id=4)
pt5 = PostTag(post_id=3, tag_id=1)
pt6 = PostTag(post_id=3, tag_id=4)
pt7 = PostTag(post_id=4, tag_id=4)
pt8 = PostTag(post_id=5, tag_id=2)
pt9 = PostTag(post_id=6, tag_id=3)
pt10 = PostTag(post_id=6, tag_id=2)

db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10])

db.session.commit()
