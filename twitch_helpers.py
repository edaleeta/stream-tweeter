"""Twitch API Helper Functions for Stream Tweeter."""

from datetime import datetime
import os
import time
import requests
from model import StreamSession, TwitchClip, User
import apscheduler_handlers as ap_handlers


TEST_ID = None  #str(80145304)


class Unauthorized(Exception):
    """Custom exception for unauthorized Twitch requests."""

    def __init__(self):
        super().__init__("Unauthorized request. User's Twitch token invalid.")

# Twitch Requirements
try:
    TWITCH_CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
    TWITCH_CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
    WEBHOOKS_BASE_URL = os.environ["WEBHOOKS_BASE_URL"]
except KeyError:
    print("Please set the environment variables.")

# Stores user_id and corresponding number of failures.
CHECK_STREAM_ONLINE_FAILURES = {}
TWITCH_API_FAILURES = {}


def create_header(user):
    """Creates a header for Twitch API calls."""
    token = user.twitch_token.access_token
    header = {"Authorization": "Bearer {}".format(token)}
    return header


def is_twitch_online(user):
    """Check if user's Twitch stream is live."""

    user_id = user.user_id
    response = get_stream_info(user)
    while TWITCH_API_FAILURES.get(user_id, 0) < 2:
        try:
            check_response_status(response, user)
            stream_data = response.json().get("data")
            # If stream_data has contents, the user is streaming.
            if stream_data:
                return True
            # Otherwise, the stream is offline.
            return False
        except Unauthorized as e:
            # If there are too many failures, stop retrying.
            if handle_check_stream_online_failures(user_id):
                return
            print(e)
            refresh_users_token(user)
        except Exception as e:
            print(e)
            return False


def check_response_status(response, user):
    """Handles errors for response status codes."""

    status_code = response.status_code

    if status_code == 200:
        print("Response OK.")
        reset_twitch_api_fail_counter(user)
        return True
    elif status_code == 401:
        # TODO: Create custom exception
        # so we can use this to refresh user's token.
        raise Unauthorized
    else:
        raise Exception("Reaching Twitch API failed. Status code: {}"
                        .format(status_code))


def reset_twitch_api_fail_counter(user):
    """Resets the Twitch API failure counter for user."""
    user_id = user.user_id
    TWITCH_API_FAILURES[user_id] = 0


def get_stream_info(user):
    """Get user's stream info from Twitch API."""

    twitch_id = str(user.twitch_id)
    payload_streams = {"user_id": TEST_ID or twitch_id,
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
    print(response.status_code)

    while TWITCH_API_FAILURES.get(user_id, 0) < 2:
        try:
            check_response_status(response, user)
            all_stream_data = response.json().get("data")
            # If the stream is offline, data will be an empty array.
            if not all_stream_data:
                # We want to increment failure counter.
                # Define a seperate function to handle that.
                handle_check_stream_online_failures(user_id)
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
            CHECK_STREAM_ONLINE_FAILURES[user_id] = 0

            return stream_data
        
        except Unauthorized as e:
            # If there are too many failures, stop retrying.
            if handle_check_stream_online_failures(user.user_id):
                return None
            print(e)
            refresh_users_token(user)

        except Exception as e:
            print(str(e))
            return None


def handle_check_stream_online_failures(user_id):
    """Handles stream offline events."""

    CHECK_STREAM_ONLINE_FAILURES[user_id] = CHECK_STREAM_ONLINE_FAILURES.get(user_id, 0) + 1
    stream_failures = CHECK_STREAM_ONLINE_FAILURES[user_id]

    if stream_failures > 1:
        print("User's {} stream is offline! \
              Ending session and jobs.".format(user_id))
        # Reset failure counter.
        CHECK_STREAM_ONLINE_FAILURES[user_id] = 0

        ap_handlers.stop_fetching_twitch_data(user_id)
        print("\n\nENDED STREAM DATA FETCH.\n\n")
        ap_handlers.stop_tweeting(user_id)
        print("\n\nENDED TWEETS.\n\n")
        return True
    else:
        print("User {}'s stream might be offline. Will try again.".format(
            user_id
        ))
        return False


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

    user = User.get_user_from_id(user_id)
    twitch_id = str(user.twitch_id)
    payload_clips = {"broadcaster_id": TEST_ID or twitch_id}  # Edit this to test
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
    while failures < 3:
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


def refresh_users_token(user):
    """Refresh user's token."""

    token_response = send_refresh_token_request(user)
    new_token = process_refresh_token_response(token_response, user)
    return new_token


def send_refresh_token_request(user):
    """Sends post request to refresh user's Twitch access token."""
    refresh_token = user.twitch_token.refresh_token

    payload = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post("https://id.twitch.tv/oauth2/token",
                             data=payload)

    print("Sent request to refresh user's token.")

    return response


def process_refresh_token_response(response, user):
    """Processes refresh token response."""

    try:
        check_response_status(response, user)
    except Exception as e:
        print(str(e))
        return
    token_data = response.json()

    new_access_token = token_data.get("access_token")
    new_refresh_token = token_data.get("refresh_token")
    new_expires_in = token_data.get("expires_in")

    user.update_twitch_access_token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        expires_in=new_expires_in
    )
    return user.twitch_token


def create_callback_url(user):
    """Creates a callback url for webhook subsubscriptions."""

    user_id = user.user_id
    url = WEBHOOKS_BASE_URL + "/api/hooks/streamstatus/" + str(user_id)
    return url


def create_webhooks_header():
    """Creates the header for a webhook subscription."""
    header = {"Client-ID": TWITCH_CLIENT_ID,
              "Content-Type": "application/json"}
    return header


def create_webhooks_payload(user):
    """Creates the payload for a webhook subscription request."""

    topic = ("https://api.twitch.tv/helix/streams?user_id=" +
             str(user.twitch_id))
    
    callback_url = create_callback_url(user)

    payload = {
        "hub.mode": "subscribe",
        "hub.topic": topic,
        "hub.callback": callback_url
    }

    return payload

def subscribe_to_user_stream_events(user):
    """Sends a request to Twitch to subscribe to user's stream events."""

    pass
    

if __name__ == "__main__":
    # Interact with db if we run this module directly.

    from server import app
    from model import connect_to_db
    connect_to_db(app)
    print("Connected to DB.")
    # For testing convinience, let's get a User object.
    me = User.query.get(4)
