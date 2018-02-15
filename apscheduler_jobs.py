"""APScheduler job functions."""

from model import User, db
import twitch_helpers


def fetch_twitch_data(user_id):
    """Job: Grab data about user's stream."""
    try:
        with db.app.app_context():
            print("Fetching stream info for {} now.".format(user_id))
            user = User.get_user_from_id(user_id)
            print(user)
            twitch_helpers.get_and_write_twitch_stream_data(user)
    except Exception as e:
        print(e)



