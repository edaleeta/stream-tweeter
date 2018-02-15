"""Twitch API Helper Functions for Yet Another Twitch Toolkit."""

import requests
from model import StreamSession
from datetime import datetime


def get_twitch_stream_data(user):
    """Get Twitch stream data for user's stream."""

    twitch_id = user.twitch_id
    token = user.twitch_token.access_token
    # For the purposes of testing, will get stream data about some other user.
    testing_twitch_id = "70801500"
    payload_streams = {"user_id": testing_twitch_id,
                       "first": 1,
                       "type": "live"}
    headers = {"Authorization": "Bearer {}".format(token)}
    r_streams = requests.get("https://api.twitch.tv/helix/streams",
                             params=payload_streams,
                             headers=headers)
    # If OK response received, save stream data.
    # Note: 401 response when a new token must be fetched.
    # TODO: Add handler for reauthorization
    if r_streams.status_code == 200:
        all_stream_data = r_streams.json().get("data")
    else:
        # Otherwise, return None.
        return None
    # If the stream is live..
    if all_stream_data:
        all_stream_data = all_stream_data[0]
        timestamp = datetime.now()
        stream_id = all_stream_data.get("id")
        streamer_id = all_stream_data.get("user_id")
        stream_title = all_stream_data.get("title")
        stream_viewer_count = all_stream_data.get("viewer_count")
        stream_started_at = all_stream_data.get("started_at")
        stream_game_id = all_stream_data.get("game_id")

        # Helper function to get game info
        stream_game_title = get_twitch_game_data(stream_game_id, headers)
        # Helper function to construct stream url
        stream_url = create_stream_url(streamer_id, headers)
        # Convert started_at str to datetime
        datetime_format = "%Y-%m-%dT%H:%M:%SZ"
        stream_started_at = datetime.strptime(stream_started_at,
                                              datetime_format)

        stream_data = {"timestamp": timestamp,
                       "stream_id": stream_id,
                       "twitch_id": streamer_id,
                       "stream_title": stream_title,
                       "viewer_count": stream_viewer_count,
                       "started_at": stream_started_at,
                       "game_id": stream_game_id,
                       "game_name": stream_game_title,
                       "url": stream_url}
        StreamSession.save_stream_session(user, stream_data)
        return stream_data
    # Else... things that happen when stream is offline.
    else:
        # TODO: Add logic to CONFIRM the stream is down before proceeding.
        print("Stream is offline!")
        StreamSession.end_stream_session(user, datetime.now())
        # TODO: End the job that is sending tweets on an interval.
        return None


def create_stream_url(twitch_id, headers):
    """Construct a URL to Twitch stream for given twitch id.
    Purposefully pulls current Twitch user data in case stored username
    is out of date."""

    # TODO: When this is triggered, also update stored value in db?

    payload = {"id": twitch_id}
    r_users = requests.get("https://api.twitch.tv/helix/users",
                           params=payload,
                           headers=headers)

    # If OK response received, store Twitch username.
    if r_users.status_code == 200:
        user_name = r_users.json().get("data")[0].get("login")
    else:
        return None

    url = "https://www.twitch.tv/{}".format(user_name)
    return url


def get_twitch_game_data(game_id, headers):
    """Sends a request to Twitch API to retrieve game info from given id."""

    payload_games = {"id": game_id}
    r_games = requests.get("https://api.twitch.tv/helix/games",
                           params=payload_games,
                           headers=headers)
    # If OK response received, save game data.
    if r_games.status_code == 200:
        game_data = r_games.json().get("data")[0]
    # Otherwise return None.
    else:
        return None
    return game_data.get("name", "")