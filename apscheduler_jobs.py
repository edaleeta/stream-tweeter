"""APScheduler job functions."""

import random
from model import User, db
import twitch_helpers
import template_helpers


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


def send_tweets(user_id):
    """Job: Sends a random tweet to user's Twitter account."""
    try:
        with db.app.app_context():
            user = User.get_user_from_id(user_id)
            templates = [template.contents for template in user.templates]
            print("\n\nAVAILABLE TEMPLATES: {}\n\n".format(templates))
            random_template = random.choice(templates)
            print("\n\nRandom template is: {}\n\n".format(random_template))

            # We're getting None back here.
            # Let's just call the function to publish to Twitter and
            # populate contents there?
            # populated_template = populate_tweet_template(
            #     random_template, user_id
            # )
            template_helpers.create_and_publish_to_twitter(random_template,
                                                           user_id)
            print("TWEET TWEETED.")

    except Exception as e:
        print(e)
