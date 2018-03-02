"""Tests for twitch_helpers."""
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
# TWITCH HELPERS TESTS
###############################################################################

# Patching response for twitch users
@mock.patch("twitch_helpers.requests.get")
def test_getting_user_when_response_is_ok(mock_get_streams):
    twitch_user = {
        "data": [
            {
                "id": "27629046016",
                "user_id": "29389795",
                "game_id": "497428",
                "community_ids": [],
                "type": "live",
                "title": "Testing the stream",
                "viewer_count": 1,
                "started_at": "2018-02-16T21:04:02Z",
                "language": "en",
                "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_pixxeltesting-{width}x{height}.jpg"
            }
        ],
        "pagination": {
            "cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MX19"
        }
    }
    # Mock will respond with 200 code status.
    # Mock has a `json()` method that returns Twitch user data
    mock_get_streams.return_value = mock.MagicMock(
        status_code=200,
        json=twitch_user)


class TwitchHelpersTestCase(TestCase):

    def setUp(self):
        """Before each test..."""

        # Connect to test db
        connect_to_db(s.app, "postgresql:///testdb", False)

        # If we stop a test midway, let's make sure there's nothing in the db
        # on the next start up.
        db.reflect()
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        db.session.commit()
        sample_data()

    def tearDown(self):
        """After every test..."""

        db.session.close()
        db.reflect()
        db.drop_all()

    twitch_token = mock.Mock(spec=m.TwitchToken,
                             access_token="imagreattoken")

    user = mock.Mock(spec=m.User,
                     twitch_token=twitch_token,
                     twitch_id=29389795,
                     user_id=4)

    def test_create_header(self):
        """Checks for accurate header creation for Twitch API requests."""

        token = "imagreattoken"
        expected_header = {"Authorization": "Bearer {}".format(token)}

        self.assertEqual(twitch_helpers.create_header(self.user),
                         expected_header)

    def test_check_response_status(self):
        """Tests checking status code of Twitch responses."""
        ok_response = mock.Mock(status_code=200)
        unauth_response = mock.Mock(status_code=401)
        bad_response = mock.Mock(status_code=500)

        self.assertTrue(twitch_helpers.check_response_status(
            ok_response, self.user
        ))
        self.assertRaises(Exception,
                          twitch_helpers.check_response_status,
                          unauth_response)
        self.assertRaises(Exception,
                          twitch_helpers.check_response_status,
                          bad_response)

    @mock.patch("twitch_helpers.requests.get")
    def test_get_stream_info(self, get_streams):
        """Checks if getting stream info works."""

        get_streams.return_value = mock.Mock(
            spec=twitch_helpers.requests.Response)

        twitch_helpers.get_stream_info(self.user)
        self.assertTrue(twitch_helpers.get_stream_info(self.user))

    @mock.patch("twitch_helpers.handle_check_stream_online_failures")
    @mock.patch("twitch_helpers.refresh_users_token")
    @mock.patch("twitch_helpers.get_stream_info")
    def test_is_twitch_online(self,
        get_streams, refresh_users_token, check_failures):
        """Checks if returning t/f is accurate for user's online status."""

        json = {
            "data": [
                {
                    "id": "27629046016",
                    "user_id": "29389795",
                    "game_id": "497428",
                    "community_ids": [],
                    "type": "live",
                    "title": "Testing the stream",
                    "viewer_count": 1,
                    "started_at": "2018-02-16T21:04:02Z",
                    "language": "en",
                    "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_pixxeltesting-{width}x{height}.jpg"
                }
            ],
            "pagination": {
                "cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MX19"
            }
        }

        # Creates mock reponse to use.
        mock_response = mock.Mock()
        mock_response.json.return_value = json
        mock_response.status_code = 200

        get_streams.return_value = mock_response
        
        # Case 1: User is online.
        self.assertTrue(twitch_helpers.is_twitch_online(self.user))

        # Case 2: User is offline.
        mock_response.json.return_value = {}
        self.assertFalse(twitch_helpers.is_twitch_online(self.user))

        # Case 3: Bad response from request
        mock_response.status_code = 401
        check_failures.side_effect = [False, True]
        self.assertFalse(twitch_helpers.is_twitch_online(self.user))
        refresh_users_token.assert_called()

    @mock.patch("twitch_helpers.ap_handlers.stop_fetching_twitch_data")
    @mock.patch("twitch_helpers.ap_handlers.stop_tweeting")
    def test_handle_check_stream_online_failures(self, stop_tweet, stop_fetch):
        """A user's stream must be seen offline twice before ending jobs."""

        user_id = self.user.user_id

        # Case 1: This is the first stream failure.
        self.assertFalse(twitch_helpers.handle_check_stream_online_failures(user_id))
        stop_fetch.assert_not_called()
        stop_tweet.assert_not_called()
        self.assertEqual(twitch_helpers.CHECK_STREAM_ONLINE_FAILURES[user_id], 1)

        # Case 2: This is the second stream failure.
        twitch_helpers.handle_check_stream_online_failures(user_id)
        stop_fetch.assert_called()
        stop_tweet.assert_called()
        self.assertEqual(twitch_helpers.CHECK_STREAM_ONLINE_FAILURES[user_id], 0)

    @mock.patch("twitch_helpers.requests.get")          
    def test_create_stream_url(self, requests_get):
        """Checks that url is constructed correctly."""

        twitch_id = self.user.twitch_id

        # Set up mock objects
        json = {"data": [{"login": "pixxeltesting"}]}
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json
        requests_get.return_value = mock_response
        
        # Case 1: Response ok
        expected_url = "https://www.twitch.tv/pixxeltesting"
        self.assertEqual(
            twitch_helpers.create_stream_url(twitch_id, self.user),
            expected_url
        )

        # Case 2: Bad response
        mock_response.status_code = 401
        self.assertIsNone(
            twitch_helpers.create_stream_url(twitch_id, self.user)
        )

    @mock.patch("twitch_helpers.requests.get") 
    def test_get_twitch_game_data(self, requests_get):
        """Checks if game data is returned correctly."""

        game_id = "123"
        game_name = "Hello Kitty Adventure Island"
        # Set up mock objects
        json = {"data": [{"name": game_name}]}
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json
        requests_get.return_value = mock_response

        # Case 1: Response ok
        self.assertEqual(twitch_helpers.get_twitch_game_data(
            game_id, self.user
        ), game_name)

        # Case 2: Bad response
        mock_response.status_code = 401
        self.assertIsNone(twitch_helpers.get_twitch_game_data(
            game_id, self.user
        ))

    @mock.patch("twitch_helpers.requests.post")
    @mock.patch("twitch_helpers.get_clip_info")
    def test_generate_twitch_clip(self, get_clip_info, requests_post):
        """Test programmatic Twitch clip creation."""

        # Set up mock objects
        clip_slug = "ToastedPotatoPandas"
        clip_url = "https://twitch.tv/clips/" + clip_slug
        clip_data = {"url": clip_url}
        create_clip_json = {"data": [{"id": clip_slug}]}
        mock_response = mock.Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = create_clip_json
        
        requests_post.return_value = mock_response
        get_clip_info.return_value = clip_data

        # Case 1: Creating a clip and getting info succeed.
        new_clip, created_url = twitch_helpers.generate_twitch_clip(
            self.user.user_id)
        self.assertEqual(created_url, clip_url)

        # Case 2: Creating a clip fails.
        get_clip_info.return_value = None

        self.assertTupleEqual(
            (None, None), twitch_helpers.generate_twitch_clip(
                self.user.user_id
            ))

    @mock.patch("twitch_helpers.time.sleep")
    @mock.patch("twitch_helpers.requests.get")
    def test_get_clip_info(self, requests_get, sleep):
        """Tests getting clip info through Twitch API."""

        clip_id = "ToastedPotatoPandas"
        # Set up mock objects
        json = {"data": ["clip_info"]}
        sleep = mock.Mock()
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json
        requests_get.return_value = mock_response
        clip_info = json.get("data")[0]

        # Case 1: Clip info is returned the first time.
        self.assertEqual(clip_info, twitch_helpers.get_clip_info(
            clip_id, self.user
        ))
        # Case 2: Clip info fails
        json = {"data": []}
        mock_response.json.return_value = json
        self.assertFalse(twitch_helpers.get_clip_info(
            clip_id, self.user
        ))

    @mock.patch("twitch_helpers.handle_check_stream_online_failures")
    @mock.patch("twitch_helpers.create_stream_url")
    @mock.patch("twitch_helpers.get_twitch_game_data")
    @mock.patch("twitch_helpers.datetime")
    @mock.patch("twitch_helpers.get_stream_info")
    def test_serialize_twitch_stream_data(self,
                                          get_stream_info,
                                          datetime_mock,
                                          get_twitch_game_data,
                                          create_stream_url,
                                          handle_failures):

        # Set up mock objects
        json_stream_info = {
            "data": [
                {
                    "id": "27739018896",
                    "user_id": "71166086",
                    "game_id": "313558",
                    "community_ids": [],
                    "type": "live",
                    "title": "deadmau5 n stuff",
                    "viewer_count": 606,
                    "started_at": "2018-02-26T13:57:26Z",
                    "language": "en",
                    "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_deadmau5-{width}x{height}.jpg"
                }
            ],
            "pagination": {
                "cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MX19"
            }
        }
        create_stream_url.return_value = "bar"
        get_twitch_game_data.return_value = "foo"
        datetime_mock.utcnow.return_value = datetime.datetime(2017, 1, 1)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_stream_info
        get_stream_info.return_value = mock_response
        datetime_format = "%Y-%m-%dT%H:%M:%SZ"
        started_at = datetime.datetime.strptime("2018-02-26T13:57:26Z",
                                                datetime_format)
        datetime_mock.strptime.return_value = datetime.datetime\
            .strptime("2018-02-26T13:57:26Z", datetime_format)

        expected_stream_data = {
            "timestamp": datetime_mock.utcnow.return_value,
            "stream_id": "27739018896",
            "twitch_id": "71166086",
            "stream_title": "deadmau5 n stuff",
            "viewer_count": 606,
            "started_at": started_at,
            "game_id": "313558",
            "game_name": "foo",
            "url": "bar"
        }

        # Case 1: Stream is online
        self.assertEqual(twitch_helpers.serialize_twitch_stream_data(
            self.user), expected_stream_data)

        # Case 2: Stream is offline.
        mock_response.json.return_value = {"data": []}
        self.assertIsNone(twitch_helpers.serialize_twitch_stream_data(
            self.user))
        handle_failures.assert_called()

    # Case 3: Handle unauthorized response.
    @mock.patch("twitch_helpers.handle_check_stream_online_failures")
    @mock.patch("twitch_helpers.get_stream_info")
    def test_serialize_twitch_stream_data_fails(self,
                                                get_stream_info,
                                                stream_failures):
        print("Testing 401!!")
        mock_response = mock.Mock()
        mock_response.status_code = 401
        get_stream_info.return_value = mock_response
        twitch_helpers.refresh_users_token = mock.Mock()

        stream_failures.side_effect = [False, True]
        self.assertIsNone(twitch_helpers.serialize_twitch_stream_data(
            self.user
        ))
        stream_failures.assert_called()

    @mock.patch("twitch_helpers.requests.post")
    def test_token_refresh_request(self, mock_post):
        """Tests token refresh request."""

        # Set up mock objects
        new_token = "foo"
        new_refresh_token = "bar"
        new_expires_in = 3600

        json = {
            "access_token": new_token,
            "refresh_token": new_refresh_token,
            "expires_in": new_expires_in,
            "scope": ["clips:edit", "user:read:email"]
            }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json
        mock_post.return_value = mock_response

        self.assertEqual(twitch_helpers.send_refresh_token_request(self.user),
                         mock_response)

    @mock.patch("twitch_helpers.check_response_status")
    def test_process_refresh_token_response(self, response_status):
        """Tests processsing a refresh token response."""

        # Sets up mock objects
        user = m.User.query.first()
        response = mock.Mock()
        response.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 14412,
            "refresh_token": "new_refresh_token",
            "scope": ["clips:edit", "user:read:email"]
        }

        # Case 1: Response status is OK
        response_status.return_value = True
        twitch_helpers.process_refresh_token_response(response, user)

        self.assertEqual(
            user.twitch_token.access_token,
            "new_access_token"
        )
        self.assertEqual(
            user.twitch_token.refresh_token,
            "new_refresh_token"
        )
        self.assertEqual(
            user.twitch_token.expires_in,
            14412
        )

    def test_process_refresh_token_response_failed(self):
        """Tests processing a refresh token when receiving a bad response."""
        response = mock.Mock()
        response.status_code = 400
        # Case 2: Reponse status is not OK
        self.assertIsNone(twitch_helpers.process_refresh_token_response(
                response, self.user))

    @mock.patch("twitch_helpers.send_refresh_token_request")
    @mock.patch("twitch_helpers.process_refresh_token_response")
    def test_refresh_users_token(self, process_response, send_request):
        "Tests refreshing user's token."
        
        twitch_helpers.refresh_users_token(self.user)
        process_response.assert_called()
        send_request.assert_called()


if __name__ == "__main__":
    import unittest
    unittest.main()