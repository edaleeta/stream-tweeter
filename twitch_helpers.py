"""Twitch API Helper Functions for Stream Tweeter."""

from datetime import datetime
import time
import requests
from model import StreamSession, TwitchClip, User
import apscheduler_handlers as ap_handlers

# Stores user_id and corresponding number of failtures.
CHECK_STREAM_FAILURES = {}


def create_header(user):
    """Creates a header for Twitch API calls."""
    token = user.twitch_token.access_token
    header = {"Authorization": "Bearer {}".format(token)}
    return header


def is_twitch_online(user):
    """Check if user's Twitch stream is live."""

    response = get_stream_info(user)
    try:
        check_response_status(response)
        stream_data = response.json().get("data")
        # If stream_data has contents, the user is streaming.
        if stream_data:
            return True
        # Otherwise, the stream is offline.
        return False
    except Exception as e:
        print(str(e))
        return False


def check_response_status(response):
    """Handles errors for response status codes."""

    status_code = response.status_code

    if status_code == 200:
        print("Response OK.")
        return True
    elif status_code == 401:
        # TODO: Create custom exception
        # so we can use this to refresh user's token.
        raise Exception("Access token expired.")
    else:
        raise Exception("Reaching Twitch API failed. Status code: {}"
                        .format(status_code))


def get_stream_info(user):
    """Get user's stream info from Twitch API."""

    twitch_id = str(user.twitch_id)
    test_id = str(37764822)
    payload_streams = {"user_id": twitch_id,    # Edit this to test
                       "first": 1,
                       "type": "live"}

    response = requests.get("https://api.twitch.tv/helix/streams",
                            params=payload_streams,
                            headers=create_header(user))
    return response


def serialize_twitch_stream_data(user):
    """Get Twitch stream data for user's stream."""
    user_id = user.user_id
    response = get_stream_info(user)

    try:
        check_response_status(response)
        all_stream_data = response.json().get("data")
    except Exception as e:
        print(str(e))
        return None

    # If the stream is offline, data will be an empty array.
    if not all_stream_data:
        # We want to increment failure counter.
        # Define a seperate function to handle that.
        handle_check_stream_failures(user_id)
        return None

    # If the stream is live...
    # print("Stream data: {}".format(all_stream_data))
    all_stream_data = all_stream_data[0]
    timestamp = datetime.utcnow()
    stream_id = all_stream_data.get("id")
    streamer_id = all_stream_data.get("user_id")
    stream_title = all_stream_data.get("title")
    stream_viewer_count = all_stream_data.get("viewer_count")
    stream_started_at = all_stream_data.get("started_at")
    stream_game_id = all_stream_data.get("game_id")

    # Helper function to get game info
    stream_game_title = get_twitch_game_data(stream_game_id, user)
    # Helper function to construct stream url
    stream_url = create_stream_url(streamer_id, user)
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
    # Reset stream failures counter to 0
    CHECK_STREAM_FAILURES[user_id] = 0

    return stream_data


def handle_check_stream_failures(user_id):
    """Handles stream offline events."""

    user = User.query.get(user_id)

    CHECK_STREAM_FAILURES[user_id] = CHECK_STREAM_FAILURES.get(user_id, 0) + 1
    stream_failures = CHECK_STREAM_FAILURES[user_id]

    if stream_failures > 1:
        print("User's {} stream is offline! \
              Ending session and jobs.".format(user_id))
        # Reset failure counter.
        CHECK_STREAM_FAILURES[user_id] = 0
        # Save end timestamp of stream session.
        StreamSession.end_stream_session(user, datetime.utcnow())
        ap_handlers.stop_tweeting(user_id)
        print("\n\nENDING TWEETS.\n\n")
        ap_handlers.stop_fetching_twitch_data(user_id)
        print("\n\nENDING STREAM DATA FETCH.\n\n")
    else:
        print("User {}'s stream might be offline. Will try again.".format(
            user_id
        ))


def write_twitch_stream_data(user, stream_data):
    """Write stream data to db."""
    StreamSession.save_stream_session(user, stream_data)


def create_stream_url(twitch_id, user):
    """Construct a URL to Twitch stream for given twitch id.
    Purposefully pulls current Twitch user data in case stored username
    is out of date."""

    # TODO: When this is triggered, also update stored value in db?

    payload = {"id": twitch_id}
    r_users = requests.get("https://api.twitch.tv/helix/users",
                           params=payload,
                           headers=create_header(user))

    # If OK response received, store Twitch username.
    if r_users.status_code == 200:
        user_name = r_users.json().get("data")[0].get("login")
    else:
        return None

    url = "https://www.twitch.tv/{}".format(user_name)
    return url


def get_twitch_game_data(game_id, user):
    """Sends a request to Twitch API to retrieve game info from given id."""

    payload_games = {"id": game_id}
    r_games = requests.get("https://api.twitch.tv/helix/games",
                           params=payload_games,
                           headers=create_header(user))
    # If OK response received, save game data.
    if r_games.status_code == 200:
        game_data = r_games.json().get("data")[0]
    # Otherwise return None.
    else:
        return None
    return game_data.get("name", "")


def generate_twitch_clip(user_id):
    """Generate a Twitch Clip from user's channel.
       Returns the URL and new clip object on success."""

    # TODO: EDIT OUT TESTING VARS
    user = User.get_user_from_id(user_id)
    twitch_id = str(user.twitch_id)
    test_id = str(37764822)
    payload_clips = {"broadcaster_id": twitch_id}
    r_clips = requests.post("https://api.twitch.tv/helix/clips",
                            data=payload_clips,
                            headers=create_header(user))
    if r_clips.status_code == 202:
        # Save the clip's slug; used as `id` in Twitch API
        clip_slug = r_clips.json().get("data")[0].get("id")
        # Send a request to Get Clips to confirm clip was created.

        clip_info = get_clip_info(clip_slug, user)
        if clip_info:
            # Store the url
            url = clip_info.get("url")
            # Save clip to DB
            new_clip = TwitchClip.save_twitch_clip(clip_slug, user_id)
            return (new_clip, url)

    # TODO: If this fails, return None.
    # Add better error handling.
    return None, None


def get_clip_info(clip_id, user):
    """Use given clip id to fetch info from Twitch API."""

    # Note: Twitch recommends giving the API 15 seconds to fetch a newly
    # created clip. If 15 seconds passes and we receive nothing, we can
    # assume that no clip was created.
    failures = 0
    payload_get_clip = {"id": clip_id}
    while failures <= 3:
        r_get_clip = requests.get("https://api.twitch.tv/helix/clips",
                                  params=payload_get_clip,
                                  headers=create_header(user))
        if r_get_clip.status_code == 200:
            clip_info = r_get_clip.json().get("data")
            try:
                clip_info = clip_info[0]
                return clip_info
            except IndexError:
                failures += 1
                time.sleep(5)
    return None

if __name__ == "__main__":
    # Interact with db if we run this module directly.

    from server import app
    from model import connect_to_db
    connect_to_db(app)
    print("Connected to DB.")
    # For testing convinience, let's get a User object.
    me = User.query.get(4)
