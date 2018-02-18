"""Tests for Yet Another Twitch Toolkit."""
from unittest import TestCase
import server as s
import model as m
import template_helpers as temp_help
from model import connect_to_db, db, sample_data

# TODO: Update this to insert example data
# then rebuild and teardown after every test.


class UserModelTestCase(TestCase):
    """Tests User class methods."""

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

    def test_get_user_from_id(self):
        """Receive a User or None for given user id."""

        user_id = 4
        user = m.User.get_user_from_id(user_id)
        self.assertEqual(user.user_id, user_id)

        user_id = 500
        user = m.User.get_user_from_id(user_id)
        self.assertIsNone(user)

    def test_get_users_from_email(self):
        """Receive a list of Users with given email."""

        # Case 1: Email exists for at least one user.
        email = "testing@test.com"
        users = m.User.get_users_from_email(email)

        found_emails = [user.email for user in users]

        for found_email in found_emails:
            self.assertEqual(email, found_email)

        # Case 2: Email does not exist for any users.
        email_not_exist = "imnotauser@nope.com"
        users = m.User.get_users_from_email(email_not_exist)
        self.assertFalse(users)

    def test_get_users_from_twitch_id(self):
        """Receive a User from given Twitch id."""

        # Case 1: Twitch id exists for a user.
        twitch_id = "29389795"
        user = m.User.get_user_from_twitch_id(twitch_id)
        self.assertEqual(twitch_id, user.twitch_id)

        # Case 2: Twitch id does not exist for any user.
        twitch_id = "1234"
        user = m.User.get_user_from_twitch_id(twitch_id)
        self.assertIsNone(user)

    def test_update_twitch_access_token(self):
        """Checks if Twitch Tokens were updated correctly."""

        # Case 1: User does not have an existing Twitch token in db.
        current_user = m.User.query.first()
        access_token = "ThisIsAGreatToken"
        refresh_token = "RefreshMePlease"
        expires_in = 6000
        current_user.update_twitch_access_token(
            access_token,
            refresh_token,
            expires_in
        )

        token = m.TwitchToken.query.filter_by(
            user_id=current_user.user_id).one()
        
        self.assertEqual(access_token, token.access_token)
        self.assertEqual(refresh_token, token.refresh_token)
        self.assertEqual(expires_in, token.expires_in)

        # Case 2: Updating token for the same user.

        new_access_token = "ImANewAccessToken"
        new_refresh_token = "ImANewRefreshToken"
        new_expires_in = 9000

        current_user.update_twitch_access_token(
            new_access_token,
            new_refresh_token,
            new_expires_in
        )

        token = m.TwitchToken.query.filter_by(
            user_id=current_user.user_id).one()

        self.assertEqual(new_access_token, token.access_token)
        self.assertEqual(new_refresh_token, token.refresh_token)
        self.assertEqual(new_expires_in, token.expires_in)


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

        temp_help.add_basic_templates(new_user)

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
