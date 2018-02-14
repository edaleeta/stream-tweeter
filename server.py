"""Yet Another Twitch Toolkit."""

import os
import string
import re
from datetime import datetime
import flask
from flask import (Flask, flash, get_template_attribute,
                   render_template, redirect,
                   request, session, url_for)
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_oauthlib.client import OAuth
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined, evalcontextfilter, Markup, escape
import requests
import tweepy
from model import *

app = Flask(__name__)

# Set so we can use Flask's default toolbar
app.secret_key = "18db2d51c63606dece6e98a196c6a262c2026c6f9cbc3e4f"

# Raise an exception if we use an undefined variable in Jinja.
app.jinja_env.undefined = StrictUndefined

# Login manager for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

###############################################################################
# Twitch OAuth2 Requirements
###############################################################################
twitch_oauth = OAuth(app)
try:
    twitch_client_id = os.environ["TWITCH_CLIENT_ID"]
except KeyError:
    print("Please set the environment variable TWITCH_CLIENT_ID")
try:
    twitch_client_secret = os.environ["TWITCH_CLIENT_SECRET"]
except KeyError:
    print("Please set the environment variable TWITCH_CLIENT_SECRET")

twitch_base_url = "https://api.twitch.tv/helix/"
twitch_authorize_url = "https://api.twitch.tv/kraken/oauth2/authorize"
twitch_access_token_url = "https://api.twitch.tv/kraken/oauth2/token"
redirect_uri = "http://localhost:7000/login-twitch-redirect"
params = {"scope": "clips:edit user:read:email"}

twitch = twitch_oauth.remote_app(
    "twitch",
    base_url=twitch_base_url,
    request_token_params=params,
    request_token_url=None,
    access_token_method="POST",
    access_token_url=twitch_access_token_url,
    authorize_url=twitch_authorize_url,
    consumer_key=twitch_client_id,
    consumer_secret=twitch_client_secret
)


###############################################################################
# Twitter Oauth Requirements
###############################################################################
TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
TWITTER_REDIRECT_URL = "http://localhost:7000/auth-twitter/authorized"

###############################################################################
# NL2BR CUSTOM JINJA FILTER
###############################################################################
# Regex for custom nlbr filter
_paragraph_re = re.compile(r'(?:\r)?')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route("/")
def show_index():
    "Show homepage."
    if current_user:
        return render_template("add-tweet-template.html")

    return render_template("index.html")


@app.route("/register-twitch")
def process_user_registration():
    """Process user creation from Twitch user info."""

    user_twitch_email = session["current_twitch_user"]["email"]
    user_twitch_id = session["current_twitch_user"]["id"]
    user_twitch_username = session["current_twitch_user"]["login"]
    user_twitch_displayname = session["current_twitch_user"]["display_name"]

    print(user_twitch_email)
    print(user_twitch_id)
    print(user_twitch_displayname)
    print(user_twitch_username)

    new_user = User(email=user_twitch_email,
                    twitch_id=user_twitch_id,
                    twitch_username=user_twitch_username,
                    twitch_displayname=user_twitch_displayname)

    db.session.add(new_user)
    db.session.commit()

    # Add base templates for user.
    add_basic_templates(new_user)
    flash("Account created successfully.")
    # Login new user
    login_user(new_user)

    # Get token info from session.
    access_token = session["twitch_access_token"]["access_token"]
    refresh_token = session["twitch_access_token"]["refresh_token"]
    expires_in = session["twitch_access_token"]["expires_in"]

    # Add token info for new user.
    current_user.update_twitch_access_token(
        access_token,
        refresh_token,
        expires_in
    )

    return redirect("/")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login page."""

    return render_template("login.html")


@app.route("/login/twitch")
def login_with_twitch():
    """Logs in user with Twitch account."""
    callback_uri = url_for("authorize_twitch", _external=True)
    return (twitch.authorize(callback=callback_uri,
                             next=request.args.get("next") or
                             request.referrer or None))


@app.route("/login/twitch/authorized")
def authorize_twitch():
    """Get access token from Twitch user after auth."""
    next_url = request.args.get('next') or url_for('show_index')
    resp = twitch.authorized_response()

    # Redirect with message if user does not authorize Twitch account.
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    session["twitch_access_token"] = resp
    access_token = session["twitch_access_token"]["access_token"]
    refresh_token = session["twitch_access_token"]["refresh_token"]
    expires_in = session["twitch_access_token"]["expires_in"]

    # Send a request to Twitch to get information about authed Twitch user.
    current_twitch_user = twitch.get("users")

    # If the response is OK...
    if current_twitch_user.status == 200:
        session["current_twitch_user"] = current_twitch_user.data["data"][0]
        current_twitch_user_id = session["current_twitch_user"]["id"]

        # Get all Twitch IDs in db
        twitch_ids = {user.twitch_id for user in User.query.all()}

        # If the user's Twitch ID is not found in db, create a user.
        if current_twitch_user_id not in twitch_ids:
            return redirect("/register-twitch")
        # Else, login the user and overwrite current access token info in db.
        # TODO: Implement overwriting access token.
        else:
            print("Twitch ID recognized. Logging you in.")
            login_user(User.get_user_from_twitch_id(current_twitch_user_id))
            current_user.update_twitch_access_token(
                access_token,
                refresh_token,
                expires_in
            )
            flask.next = request.args.get('next')
            return redirect(flask.next or url_for('show_index'))


@app.route("/logout")
def logout_user_cleanup():
    """Logs out user."""

    logout_user()
    session.clear()

    flash("You were logged out!")
    return redirect("/")


@app.route("/add-tweet-template", methods=["POST"])
def add_user_created_template():
    """Adds template the current user created to DB."""
    # TODO: Handle trimming of whitespace and validation post trim in JS
    template_contents = request.form.get("contents", "").strip()
    if template_contents:
        # TODO: Need to add messaging that plays nicely with AJAX.
        # flash("You entered something!")
        add_template_to_db(current_user, template_contents)
    else:
        # flash("You didn't enter anything.")
        return redirect("/")

    tweet_template_list = get_template_attribute("macros.html",
                                                 "tweet_template_list")
    return tweet_template_list(current_user)


@app.route("/delete-tweet-template", methods=["POST"])
def delete_template_for_user():
    """Deletes a specific template owned by user."""

    temp_to_del = request.form.get("template_id")
    current_user.delete_template(temp_to_del)

    tweet_template_list = get_template_attribute("macros.html",
                                                 "tweet_template_list")
    return tweet_template_list(current_user)


@app.route("/edit-tweet-template", methods=["POST"])
def edit_template_for_user():
    """Edits a specific template owned by a user."""
    # TODO: Handle trimming of whitespace and validation post trim in JS
    temp_to_edit = request.form.get("template_id").strip()
    contents = request.form.get("contents")

    current_user.edit_template(temp_to_edit, contents)

    tweet_template_list = get_template_attribute("macros.html",
                                                 "tweet_template_list")

    return tweet_template_list(current_user)


@app.route("/send-test-tweet", methods=["POST"])
def send_test_tweet():
    """Sends a test tweet using received tweet template id."""

    template_id = request.form.get("template_id")
    template_contents = Template.get_template_from_id(template_id).contents

    # Fill in tweet template with data.
    # TODO: Edit this function to use data from Twitch API
    populated_tweet_template = populate_tweet_template(template_contents,
                                                       current_user)
    if populated_tweet_template:
    # Post the tweet to Twitter
    # TODO: UNCOMMENT WHEN DONE TESTING TWITCH API
    #
        # publish_to_twitter(populated_tweet_template,
        #                    current_user.twitter_token.access_token,
        #                    current_user.twitter_token.access_token_secret,
        #                    current_user.user_id)

        # Currently sending back the populated tweet for confirmation alert.abs
        return populated_tweet_template
    # TODO: Error handler for case when stream is offline.
    return "Stream is offline."


@app.route("/auth-twitter")
def authorize_twitter():
    """Authorize a user's Twitter account."""

    twitter_oauth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                        TWITTER_CONSUMER_SECRET,
                                        TWITTER_REDIRECT_URL)

    try:
        redirect_url = twitter_oauth.get_authorization_url()
        session["twitter_request_token"] = twitter_oauth.request_token
        return redirect(redirect_url)
    except tweepy.TweepError:
        # TODO: Set up a handler for auth errors.
        flash("Authorization failed.")
        return redirect("/")


@app.route("/auth-twitter/authorized")
def get_twitter_token():
    """Get access token and secret from Twitter user after auth."""

    twitter_oauth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                        TWITTER_CONSUMER_SECRET)

    verifier = request.args.get("oauth_verifier")
    request_token = session.get("twitter_request_token")
    session.pop("twitter_request_token", None)
    # Note: In the app's current structure it isn't necessary to rebuild from
    # session; More for future proofing if/when token handler moves.
    twitter_oauth.request_token = request_token

    try:
        twitter_oauth.get_access_token(verifier)
        access_token = twitter_oauth.access_token
        access_token_secret = twitter_oauth.access_token_secret
        print(access_token)
        print(access_token_secret)
        current_user.update_twitter_access_token(access_token,
                                                 access_token_secret)
        flash("Twitter account connected.")
    except tweepy.TweepError:
        flash("Authorization failed.")

    return redirect("/")

###############################################################################
# TEST ROUTES
###############################################################################


@app.route("/webhooktest", methods=["POST"])
def test_webhook():
    """Prints webhook response payload. """
    print("Webhook Request: {}".format(request.get_json()))
    print("User stream state has changed.")

    return ('', 204)


@app.route("/webhooktest", methods=["GET"])
def test_webhook_get():
    """Echos back challenge for subscribing."""
    print("Webhook Request: {}".format(list(request.args.items())))

    if request.args.get("hub.mode") == "subscribe":
        print("Successfully subscribed to webhook.")
        return (request.args.get("hub.challenge"))
    else:
        print("Subscription to webhook unsuccessful.")
        return ('', 204)


@twitch.tokengetter
def twitch_tokengetter():
    return session.get('twitch_access_token')

###############################################################################
# HELPER FUNCTIONS
###############################################################################


@login_manager.user_loader
def load_user(user_id):
    """Loads user from db. user_id must be unicode."""

    print("Found user {}".format(User.query.get(user_id)))
    return User.query.get(user_id)


def add_template_to_db(user, temp_contents):
    """Adds a user-created template to db for user."""

    new_template = Template(user_id=user.user_id, contents=temp_contents)
    db.session.add(new_template)
    db.session.commit()


def is_email_exists(submitted_email):
    """Check if email is already registered."""

    emails = db.session.query(User.email).all()

    for email in emails:
        if submitted_email in email:
            return True
    return False


def add_basic_templates(this_user):
    """Add basic templates for current user."""

    base_templates = BaseTemplate.query

    temps_to_add = [(Template(user_id=this_user.user_id,
                              contents=base_template.contents))
                    for base_template in base_templates]

    db.session.bulk_save_objects(temps_to_add)
    db.session.commit()


def populate_tweet_template(contents, user):
    """Inserts data into placeholders."""

    data_for_template = get_twitch_template_data(user)
    if data_for_template:
        tweet_template = string.Template(contents)
        populated_template = tweet_template.safe_substitute(data_for_template)
        return populated_template
    # TODO: Error handler for case when stream is offline.
    return None


def get_twitch_template_data(user):
    """Creates a dictionary to use for tweet template filler."""

    all_stream_data = get_twitch_stream_data(user)
    if all_stream_data:
        stream_template_data = {"url": all_stream_data["url"],
                                "game": all_stream_data["game_name"],
                                "stream_title": all_stream_data["stream_title"],
                                "viewers": all_stream_data["viewer_count"]}
        return stream_template_data
    # TODO: Error handler for case when stream is offline.
    return None


def get_twitch_stream_data(user):
    """Get Twitch stream data for user's stream."""

    twitch_id = user.twitch_id
    token = user.twitch_token.access_token
    # For the purposes of testing, will get stream data about some other user.
    testing_twitch_id = "65171890"
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
    # TODO: DELETE THIS AFTER TESTING OFFLINE CASE.
    all_stream_data = []    # REMOVE THIS LINE AFTER TESTING.
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
        print("Stream is offline!")
        # TODO: We'll want to update the most recent stream session for user's
        # ended_at
        # We'll want to end the job that is sending tweets on an interval.
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


def publish_to_twitter(content, access_token,
                       access_token_secret, user_id):
    """Publishes given content to a user's Twitter account."""
    twitter_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                       TWITTER_CONSUMER_SECRET)
    twitter_auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(twitter_auth)

    try:
        # Send Tweet and catch response
        response = api.update_status(content)
        # Store sent tweet data in db
        SentTweet.store_sent_tweet(response, user_id)
    except tweepy.TweepError as error:
        # TODO: Set up better handler for errors.
        print(error.reason)


if __name__ == "__main__":
    # Debug mode enabled for Flask Debug Toolbar
    app.debug = True
    # Don't cache templates.
    app.jinja_env.auto_reload = app.debug

    # Connect to db
    connect_to_db(app)

    # Use Debug Toolbar
    DebugToolbarExtension(app)

    # Run the app
    app.run(port=7000, host='0.0.0.0')
