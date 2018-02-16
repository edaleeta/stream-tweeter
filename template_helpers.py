"""Template related helpers."""

import os
import string
import twitch_helpers as twitch
import tweepy
from model import User, SentTweet

###############################################################################
# Twitter Oauth Requirements
###############################################################################
TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]


def populate_tweet_template(contents, user_id):
    """Inserts data into placeholders."""
    try:
        user = User.get_user_from_id(user_id)
        print("User ID: {}".format(user_id))

        print("\n\nI'M TRYING TO POPULATE A TWEET\n\n")

        data_for_template = get_twitch_template_data(user)

        print("\n\nDATA FOR MY TEMPLATE.\n{}".format(data_for_template))

        if data_for_template:
            tweet_template = string.Template(contents)
            populated_template = tweet_template.safe_substitute(data_for_template)

            print("\n\nPOPULATED TEMPLATE IS:\n{}".format(populated_template))

            return populated_template

        # TODO: Error handler for case when stream is offline.
        print("\n\nAM I SOMEHOW GETTING HERE!?!?\n\n")  # No.
        return None
    except Exception as e:
        print(e)


def get_twitch_template_data(user):
    """Creates a dictionary to use for tweet template filler."""

    all_stream_data = twitch.get_and_write_twitch_stream_data(user)
    if all_stream_data:
        stream_template_data = {
            "url": all_stream_data["url"],
            "game": all_stream_data["game_name"],
            "stream_title": all_stream_data["stream_title"],
            "viewers": all_stream_data["viewer_count"],
            "timestamp": all_stream_data["timestamp"]
        }

        print("I'M GETTING TWITCH TEMPLATE DATA.")
        print(stream_template_data)

        return stream_template_data
    # TODO: Error handler for case when stream is offline.
    return None


def create_and_publish_to_twitter(template, user_id):
    """Publishes given content to a user's Twitter account."""
    
    # Set up Twitter requirements
    user = User.get_user_from_id(user_id)
    token = user.twitter_token
    access_token = token.access_token
    access_token_secret = token.access_token_secret
    contents = populate_tweet_template(template, user_id)

    twitter_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                       TWITTER_CONSUMER_SECRET)
    twitter_auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(twitter_auth)

    # Clip id defaults to None.
    clip_id = None
    # Try to generate a Twitch Clip
    new_clip, clip_url = twitch.generate_twitch_clip(user_id)

    # If new clip is created, append to tweet and save clip id.
    if new_clip:
        contents += "\n{}".format(clip_url)
        clip_id = new_clip.clip_id

    try:
        # Send Tweet and catch response
        response = api.update_status(contents)
        # Store sent tweet data in db
        SentTweet.store_sent_tweet(response, user_id, clip_id=clip_id)
    except tweepy.TweepError as error:
        # TODO: Set up better handler for errors.
        print(error.reason)


if __name__ == "__main__":
    # Interact with db if we run this module directly.

    from server import app
    from model import connect_to_db
    connect_to_db(app)
    print("Connected to DB.")