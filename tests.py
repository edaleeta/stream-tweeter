"""Tests for Yet Another Twitch Toolkit."""
from unittest import TestCase
import server
from model import connect_to_db, db, sample_data

# TODO: Update this to insert example data
# then rebuild and teardown after every test.


class RegisterUserTestCase(TestCase):
    """Tests logic for user registration."""
    def setUp(self):
        """Before each test..."""

        # Connect to test db
        connect_to_db(server.app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        db.session.commit()
        sample_data()

    def tearDown(self):
        """After every test..."""

        db.session.close()
        db.drop_all()

    def test_is_email_exists(self):

        """Check if dummy emails exist or not in db."""
        assert server.is_email_exists('test@testing.com') is True
        assert server.is_email_exists('notfound@notfound.com') is False

if __name__ == "__main__":
    import unittest
    unittest.main()
