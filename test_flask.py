from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_users_23-1_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
    """Tests for routes of blogly app."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="Name")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_root_redirect(self):
        """Testing for the root route to redirect into /users"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)

    def test_show_user(self):
        """Testing for the users image and buttons to display as long as id is correct"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Name</h1>', html)
            self.assertIn('<button>Edit</button>', html)

    def test_edit_user_get_request(self):
        """Testing for the edit form to display"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)
            self.assertIn('<input type="text" name="image_url" />', html)
            self.assertIn('<button>Cancel</button>', html)

    def test_edit_user_post_request(self):
        """Testing for the post request to edit a user and change the data in our database"""

        data = {'first_name': 'New', 'last_name': 'Name',
                'image_url': 'https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg'}

        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>New Name</h1>', html)
            self.assertIn('<button>Edit</button>', html)

    def test_create_user_get_request(self):
        """Testing for the create user form to display"""
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)
            self.assertIn('<form action="/users/new" method="POST">', html)
            self.assertIn('<button>Cancel</button>', html)

    def test_create_user_post_request(self):
        """Testing for the create user post request to insert a new user into our database and update the user's listdisplayed"""

        data = {'first_name': 'Second', 'last_name': 'User',
                'image_url': 'https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg'}

        with app.test_client() as client:
            resp = client.post(f"/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('Second User', html)
            self.assertIn('Add user', html)
