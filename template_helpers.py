"""Template related helpers."""

import os
import string
import tweepy
import twitch_helpers as twitch
from model import db, BaseTemplate, SentTweet, Template, User

###############################################################################
# Twitter Oauth Requirements
###############################################################################
TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]


def add_basic_templates(user):
    """Add basic templates for user."""

    base_templates = BaseTemplate.query

    temps_to_add = [(Template(user_id=user.user_id,
                              contents=base_template.contents))
                    for base_template in base_templates]

    db.session.bulk_save_objects(temps_to_add)
    db.session.commit()


def replace_nl_with_carriage(content):
    """Turns new lines into carriage return + new line."""

    split_content = content.split("\n")
    joined_content = "\r\n".join(split_content)

    return joined_content


def populate_tweet_template(contents, user_id):
    """Inserts data into placeholders."""
    try:
        user = User.get_user_from_id(user_id)
        print("User ID: {}".format(user_id))

        print("\n\nTrying to populate tweet template with data.\n\n")

        data_for_template = get_twitch_template_data(user)

        if not data_for_template:
            print("\n\nNO DATA RECEIVED. Stream may be offline.\n\n")
            return None

        print("\n\nData for template.\n{}".format(data_for_template))
        tweet_template = string.Template(contents)
        populated_template = tweet_template.safe_substitute(
            data_for_template)

        print("\n\nPopulated template:\n{}".format(populated_template))

        return populated_template

        
    except Exception as e:
        print(e)


def get_twitch_template_data(user):
    """Creates a dictionary to use for tweet template filler."""

    all_stream_data = twitch.serialize_twitch_stream_data(user)
    if all_stream_data:
        stream_template_data = {
            "url": all_stream_data["url"],
            "game": all_stream_data["game_name"],
            "stream_title": all_stream_data["stream_title"],
            "viewers": all_stream_data["viewer_count"],
            "timestamp": all_stream_data["timestamp"]
        }
        print("RETURNING TWITCH TEMPLATE DATA.")
        print(stream_template_data)
        return stream_template_data
    print("NO DATA RETURNED FROM TWITCH. STREAM MAY BE OFFLINE.")
    return None


def publish_to_twitter(contents, user_id):
    """Publishes given content to a user's Twitter account."""

    # If given empty contents
    if not contents:
        return

    # Set up Twitter requirements
    user = User.get_user_from_id(user_id)
    token = user.twitter_token
    access_token = token.access_token
    access_token_secret = token.access_token_secret

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
    print("\n\nABOUT TO SEND A TWEET!\n\n")
    try:
        # Send Tweet and catch response
        response = api.update_status(contents)
        # Store sent tweet data in db
        SentTweet.store_sent_tweet(response, user_id, clip_id=clip_id)
        print("TWEET TWEETED.")
        return
    except tweepy.TweepError as error:
        # TODO: Set up better handler for errors.
        print(error.reason)


if __name__ == "__main__":
    # Interact with db if we run this module directly.

    from server import app
    from model import connect_to_db
    connect_to_db(app)
    print("Connected to DB.")
