"""APScheduler job functions."""

from model import User, db
from twitch_helpers import get_and_write_twitch_stream_data
from app_globals import scheduler


def start_fetching_twitch_data(user_id):
    """Begin fetching data about a user's stream."""

    print(user_id)
    scheduler.add_job(func=fetch_twitch_data,
                      id=str(user_id),
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      seconds=10)


def stop_fetching_twitch_data(user_id):
    scheduler.remove_job(str(user_id))


def fetch_twitch_data(user_id):
    """Job: Grab data about user's stream."""
    try:
        with db.app.app_context():
            print("Fetching stream info for {} now.".format(user_id))
            user = User.get_user_from_id(user_id)
            print(user)
            get_and_write_twitch_stream_data(user)
    except Exception as e:
        print(e)



