"""Tests for Yet Another Twitch Toolkit."""
from unittest import TestCase, mock
from io import StringIO
import datetime
import sqlalchemy
import server as s
import model as m
from model import connect_to_db, db
from seed_testdb import sample_data
import template_helpers as temp_help
import twitch_helpers


###############################################################################
# MODEL TESTS
###############################################################################


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
        db.reflect()
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

    def test_update_twitter_access_token(self):
        """Checks if Twitter tokens are updated correctly."""

        user = m.User.query.first()
        access_token = "ThisIsAGreatToken"
        token_secret = "ImAGoodSecret"

        # Case 1: User does not have a Twitter token in the db.
        user.update_twitter_access_token(access_token, token_secret)
        token = m.TwitterToken.query.filter_by(user_id=user.user_id).one()

        self.assertEqual(access_token, token.access_token)
        self.assertEqual(token_secret, token.access_token_secret)

        # Case 2: Updating token for the same user.abs
        new_access_token = "ImANewAccessToken"
        new_token_secret = "ImANewTokenSecret"
        user.update_twitter_access_token(new_access_token, new_token_secret)
        token = m.TwitterToken.query.filter_by(user_id=user.user_id).one()

        self.assertEqual(new_access_token, token.access_token)
        self.assertEqual(new_token_secret, token.access_token_secret)

    def test_delete_template(self):
        """Checks if user can delete a template they own and not some other."""

        user = m.User.query.first()
        # Adding another user.
        other_user = m.User(twitch_id="0987")
        m.db.session.add(other_user)
        m.db.session.commit()

        # Adding a template for the other user.
        template = m.Template(user_id=other_user.user_id,
                              contents="Hello!")
        m.db.session.add(template)
        m.db.session.commit()

        # Case 1: User deletes their own template.
        user.delete_template(10)
        is_template = m.Template.query.get(10)

        self.assertIsNone = is_template

        # Case 2: User tries to delete a template they don't own.
        self.assertRaises(sqlalchemy.orm.exc.NoResultFound,
                          user.delete_template,
                          template.template_id)

        # Case 3: User tries to delete a template that doesn't exist.
        self.assertRaises(sqlalchemy.orm.exc.NoResultFound,
                          user.delete_template,
                          600)

    def test_edit_template(self):
        """Checks if a user can update a given template."""

        new_contents = "I love cats."
        user = m.User.query.first()
        template_id = m.Template.query.filter_by(
            user_id=user.user_id).first().template_id

        user.edit_template(template_id, new_contents)
        edited_template = m.Template.query.get(template_id)
        self.assertEqual(new_contents, edited_template.contents)


class TemplateModelTestCase(TestCase):
    """Tests Template class methods."""

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
        db.reflect()
        db.drop_all()

    def test_get_template_from_id(self):
        """Get a template object or None with given template id."""

        # Case 1: Template exists.
        template = m.Template.get_template_from_id(10)
        self.assertEqual(10, template.template_id)

        # Case 2: Template doesn't exist
        template = m.Template.get_template_from_id(9000)
        self.assertIsNone(template)


class SentTweetModelTestCase(TestCase):
    """Tests SentTweet class methods."""

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
        db.reflect()
        db.drop_all()

    def test_store_sent_tweet(self):
        """Checks to see if sent tweet was saved correctly."""

        mock_id_str = "12345"
        mock_created_at = datetime.datetime(2017, 2, 14, 12, 30, 10)
        mock_text = "I tweeted a thing!"
        mock_user_id = "987"

        @mock.patch("template_helpers.tweepy.Status")
        def get_mocked_status(mocked_status):
            mocked_status.id_str = mock_id_str
            mocked_status.created_at = mock_created_at
            mocked_status.text = mock_text
            mocked_status.user.id_str = mock_user_id

            return mocked_status

        mocked_status = get_mocked_status()
        user_id = 4
        clip_id = 9

        saved_tweet = m.SentTweet.store_sent_tweet(mocked_status,
                                                   user_id,
                                                   clip_id)

        self.assertEqual(saved_tweet.user_id, user_id)
        self.assertEqual(saved_tweet.permalink,
                         "https://twitter.com/{}/status/{}".format(
                             mock_user_id, mock_id_str
                         ))
        self.assertEqual(saved_tweet.clip_id, clip_id)


class StreamSessionModelTestCase(TestCase):
    """Tests Template class methods."""

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
        db.reflect()
        db.drop_all()

    def test_save_stream_session(self):
        """Checks to see if stream session and data was saved correctly."""

        timestamp = datetime.datetime(2017, 2, 14, 12, 30, 10)
        stream_id = "1"
        streamer_id = "pixxeltesting"
        stream_title = "Best stream ever!"
        stream_viewer_count = 100
        stream_started_at = datetime.datetime(2017, 2, 14, 12, 30, 10)
        stream_game_id = "1"
        stream_game_title = "Stardew Valley"
        stream_url = "https://twitch.tv/pixxeltesting"

        stream_data = {"timestamp": timestamp,
                       "stream_id": stream_id,
                       "twitch_id": streamer_id,
                       "stream_title": stream_title,
                       "viewer_count": stream_viewer_count,
                       "started_at": stream_started_at,
                       "game_id": stream_game_id,
                       "game_name": stream_game_title,
                       "url": stream_url}

        user = m.User.query.first()

        # Case 1: Stream session does not exist for user.
        twitch_session = m.StreamSession.save_stream_session(
            user=user, stream_data=stream_data
        )
        new_data = m.StreamDatum.query.filter_by(
            stream_id=twitch_session.stream_id
        ).first()
        self.assertEqual(twitch_session.twitch_session_id, stream_id)
        self.assertEqual(new_data.timestamp, twitch_session.started_at)

        # Case 2: Stream session exists for user.
        repeat_twitch_session = m.StreamSession.save_stream_session(
            user=user, stream_data=stream_data
        )
        num_data = len(m.StreamDatum.query.filter_by(
            stream_id=twitch_session.stream_id
        ).all())
        self.assertEqual(repeat_twitch_session, twitch_session)
        self.assertEqual(num_data, 2)

    def test_end_stream_session(self):
        """Checks if an open session is closed."""

        user = m.User.query.first()
        # Alter the most recent session so it's detected as 'open'
        last_session = user.sessions[-1]
        last_session.ended_at = None
        db.session.commit()

        # Case 1: Open session is found.
        end_session_time = datetime.datetime(2017, 2, 14, 12, 30, 10)

        ended_session = m.StreamSession.end_stream_session(
            user=user, timestamp=end_session_time
        )

        self.assertEqual(last_session.ended_at, end_session_time)
        self.assertEqual(last_session, ended_session)

        # Case 2: Sessions are closed.
        self.assertIsNone(m.StreamSession.end_stream_session(
            user=user, timestamp=end_session_time
        ))


class TwitchClipModelTestCase(TestCase):
    """Tests TwitchClip class methods."""

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
        db.reflect()
        db.drop_all()

    def test_save_twitch_clip(self):
        """Checks if Twitch clip is saved correctly."""

        user = m.User.query.first()
        user_id = user.user_id
        slug = "TotallyAwesomePandas"

        # Case 1: All sessions closed. Associated stream should be most recent.
        saved_clip = m.TwitchClip.save_twitch_clip(
            slug, user_id
        )

        self.assertEqual(saved_clip.stream_id, user.sessions[-1].stream_id)

        # Case 2: Most recent session is open.
        # Alter the most recent session so it's detected as 'open'
        last_session = user.sessions[-1]
        last_session.ended_at = None
        db.session.commit()

        saved_clip = m.TwitchClip.save_twitch_clip(
            slug, user_id
        )
        self.assertEqual(saved_clip.stream_id, last_session.stream_id)

###############################################################################
# TEMPLATE HELPER TESTS
###############################################################################


class TemplateHelpersTestCase(TestCase):
    """Tests for template helpers functions."""

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
        db.reflect()
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

    def test_get_twitch_template_data(self):
        """Checks thats twitch data is being transformed correctly."""

        user = m.User.query.first()
        timestamp = datetime.datetime(2017, 2, 14, 12, 30, 10)
        stream_id = "1"
        streamer_id = "pixxeltesting"
        stream_title = "Best stream ever!"
        stream_viewer_count = 100
        stream_started_at = datetime.datetime(2017, 2, 14, 12, 30, 10)
        stream_game_id = "1"
        stream_game_title = "Stardew Valley"
        stream_url = "https://twitch.tv/pixxeltesting"

        # Case 1: Stream is online
        # Mocking data
        twitch_helpers.get_and_write_twitch_stream_data = mock.MagicMock(
            return_value={
                "timestamp": timestamp,
                "stream_id": stream_id,
                "twitch_id": streamer_id,
                "stream_title": stream_title,
                "viewer_count": stream_viewer_count,
                "started_at": stream_started_at,
                "game_id": stream_game_id,
                "game_name": stream_game_title,
                "url": stream_url
            })

        template_data = temp_help.get_twitch_template_data(user)
        self.assertEqual(template_data["url"], stream_url)
        self.assertEqual(template_data["game"], stream_game_title)
        self.assertEqual(template_data["stream_title"], stream_title)
        self.assertEqual(template_data["viewers"], stream_viewer_count)
        self.assertEqual(template_data["timestamp"], timestamp)

        # Case 2: Stream is offline
        twitch_helpers.get_and_write_twitch_stream_data = mock.MagicMock(
            return_value=None)

        template_data = temp_help.get_twitch_template_data(user)
        self.assertIsNone(template_data)



if __name__ == "__main__":
    import unittest
    unittest.main()
