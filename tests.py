"""Tests for Yet Another Twitch Toolkit."""
from unittest import TestCase
import server as s
from model import connect_to_db, db, sample_data

# TODO: Update this to insert example data
# then rebuild and teardown after every test.


class RegisterUserTestCase(TestCase):
    """Tests logic for user registration."""
    def setUp(self):
        """Before each test..."""

        # Connect to test db
        connect_to_db(s.app, "postgresql:///testdb", False)

        # Create tables and add sample data
        db.create_all()
        db.session.commit()
        sample_data()

    def tearDown(self):
        """After every test..."""

        db.session.close()
        db.drop_all()

    def test_add_basic_templates(self):
        """Check if appropriate templates are associated with new user."""

        submitted_email = "basictemplate@test.com"
        new_user = s.User(email=submitted_email, password="foo")
        db.session.add(new_user)
        db.session.commit()

        s.add_basic_templates(new_user)

        added_template_ids = [template.template_id
                              for template in s.UserTemplate.query
                              .filter_by(user_id=new_user.user_id)]

        self.assertIn(1, added_template_ids)
        self.assertIn(2, added_template_ids)
        self.assertNotIn(3, added_template_ids)


if __name__ == "__main__":
    import unittest
    unittest.main()
