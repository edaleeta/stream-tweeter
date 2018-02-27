"""APScheduler job functions."""

import random
from model import User, db
import twitch_helpers
import template_helpers


def fetch_twitch_data(user_id):
    """Job: Grab data about user's stream. Write it to db."""
    try:
        with db.app.app_context():
            print("Fetching stream info for {} now.".format(user_id))
            user = User.get_user_from_id(user_id)
            stream_data = twitch_helpers.serialize_twitch_stream_data(user)
            print(stream_data)
            if stream_data:
                twitch_helpers.write_twitch_stream_data(user, stream_data)
    except Exception as e:
        print(e)


def send_tweets(user_id):
    """Job: Sends a random tweet to user's Twitter account."""
    try:
        with db.app.app_context():
            user = User.get_user_from_id(user_id)
            templates = [template.contents for template in user.templates]
            print("\n\nAVAILABLE TEMPLATES: {}\n\n".format(templates))
            random_template = random.choice(templates)
            print("\n\nRandom template is: {}\n\n".format(random_template))

            print(template_helpers.populate_tweet_template(random_template, user_id))

            # TODO: UNCOMMENT AFTER TESTING.
            # template_helpers.create_and_publish_to_twitter(random_template,
            #                                                user_id)
            print("TWEET TWEETED.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Interact with db if we run this module directly.

    from server import app
    from model import connect_to_db
    connect_to_db(app)
    print("Connected to DB.")