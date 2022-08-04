from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_users_23-1_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_get_full_name(self):
        """Testing for 'full_name' function"""
        user = User(first_name="Test", last_name="Name")
        self.assertEquals(user.get_full_name(), "Test Name")

    def test_default_profile_image(self):
        """Testing if the default image url is set when the user is committed to the database"""
        user = User(first_name="Test", last_name="Name")

        db.session.add(user)
        db.session.commit()

        test_user = User.query.filter(user.id == 1).all()

        self.assertEquals(
            test_user[0].image_url, "https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg")
