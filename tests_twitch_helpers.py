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
def test_getting_user_when_response_is_ok(mock_get_user):
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
    mock_get_user.return_value.status_code = 200
    mock_get_user.return_value.json.return_value = twitch_user


class TwitchHelpersTestCase(TestCase):

    twitch_token = mock.Mock(spec=m.TwitchToken,
                             access_token="imagreattoken")

    user = mock.Mock(spec=m.User,
                     twitch_token=twitch_token)

    def test_create_header(self):
        """Checks for accurate header creation for Twitch API requests."""

        token = "imagreattoken"
        expected_header = {"Authorization": "Bearer {}".format(token)}

        self.assertEqual(twitch_helpers.create_header(self.user),
                         expected_header)


if __name__ == "__main__":
    import unittest
    unittest.main()