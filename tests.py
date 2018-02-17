"""Tests for Yet Another Twitch Toolkit."""
from unittest import TestCase
import server as s
import model as m
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

        mock_twitch_id = '123456'
        new_user = m.User(twitch_id=mock_twitch_id)
        db.session.add(new_user)
        db.session.commit()

        base_template_contents = [template.contents
                                  for template in m.BaseTemplate.query]

        s.add_basic_templates(new_user)

        # Get the template contents for the newly added user.
        added_template_contents = [template.contents
                                   for template in m.Template.query
                                   .filter_by(user_id=new_user.user_id)]

        # Ensure the original base templates are found for the user
        for content in base_template_contents:
            self.assertIn(content, added_template_contents)


if __name__ == "__main__":
    import unittest
    unittest.main()
