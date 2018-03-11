"""Yet Another Twitch Toolkit."""

import os
import re
import datetime
import flask
from flask import (Flask, flash, get_template_attribute,
                   render_template, redirect,
                   request, session, url_for, make_response)
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_oauthlib.client import OAuth
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined, evalcontextfilter, Markup, escape
import tweepy
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from model import *
# FOR APSCHEDULER
import apscheduler_handlers as handler
import template_helpers as temp_help
import twitch_helpers
import api_helpers
# Trying threading!
from threading import Thread

app = Flask(__name__)

# Set so we can use Flask's default toolbar
app.secret_key = "18db2d51c63606dece6e98a196c6a262c2026c6f9cbc3e4f"

# Raise an exception if we use an undefined variable in Jinja.
app.jinja_env.undefined = StrictUndefined

# Login manager for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

# APScheduler
# scheduler = APScheduler()


# DEBUGGING FOR OAUTH LIB
import sys
import logging
log = logging.getLogger('flask_oauthlib')
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True
    print("Session:", session)
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

###############################################################################
# NL2BR CUSTOM JINJA FILTER
###############################################################################
# Regex for custom nlbr filter
_paragraph_re = re.compile(r'(?:\r)?')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

###############################################################################
# API ROUTES
###############################################################################


@app.route("/api/current-user.json")
def get_current_user_json():
    "Return jsonified info about current user."

    print("Current user is: ", current_user)
    if current_user.is_authenticated:
        # Add basic user details.
        print("User is authenticated.")
        user_details = {
            "userId": current_user.user_id,
            "email": current_user.email,
            "twitchDisplayName": current_user.twitch_displayname,
            "twitchId": current_user.twitch_id,
            "tweetInterval": current_user.tweet_interval or 30,
            "isTweeting": current_user.is_tweeting
        }

        # Add status of Twitter auth
        # TODO: Will also want to check if user's token is still valid.
        if current_user.twitter_token:
            user_details["isTwitterAuth"] = True
        else:
            user_details["isTwitterAuth"] = False

        return jsonify(user_details)
    else:
        print("User is not logged in.")
        return jsonify(error="Not logged in.")


@app.route("/api/current-user.json", methods=["PUT"])
def update_current_user():
    """Updates current user's settings."""
    # TODO: Consolidate with updating tweet interval.
    if current_user.is_authenticated:
        # Update is_tweeting setting for user.
        new_is_tweeting = request.get_json().get("isTweeting")
        if isinstance(new_is_tweeting, bool):
            current_user.update_is_tweeting(new_is_tweeting)
            print("User {}'s is_tweeting set to {}.".format(
                current_user.user_id, new_is_tweeting
            ))
            # If the user enabled tweeting, renew webhook subscription.
            if new_is_tweeting:
                twitch_helpers.subscribe_to_user_stream_events(current_user)
                # Start or replace job to renew every 9 days.
                handler.renew_webhook(current_user.user_id)
            
            # If the user disabled tweeting, end tweeting job.
            # Also let the webhook expire.
            if not new_is_tweeting:
                handler.stop_tweeting(current_user.user_id)
                handler.stop_renew_webhook(current_user.user_id)

            return jsonify(success=True)

    error_message = "Bad request."
    print(error_message)
    return (flask.json.dumps({"error": error_message}),
            400,
            {'ContentType': 'application/json'})


@app.route("/api/current-user-templates.json")
def get_current_user_templates():
    """Return jsonified info about current user's templates."""

    templates = []

    for template in current_user.templates:
        template_obj = {"templateId": template.template_id,
                        "contents": template.contents}
        templates.append(template_obj)

    # return jsonify(templates)
    return jsonify(templates)


# Modified from original route for React frontend.
@app.route("/api/add-tweet-template", methods=["POST"])
def add_user_created_template_react():
    """Adds template the current user created to DB."""

    print("\n\nTRYING TO SAVE NEW TWEET TEMPLATE.\n\n")
    template_contents = request.get_json().get("contents", "")

    print("Submitted contents: {}".format(template_contents))
    if template_contents:
        template_contents = temp_help.replace_nl_with_carriage(
            template_contents
        )
        # TODO: Need to add messaging that plays nicely with AJAX.
        # flash("You entered something!")
        add_template_to_db(current_user, template_contents)
        return (flask.json.dumps({'success': True}),
                200,
                {'ContentType': 'application/json'})

    error_message = "Did not receive template contents."
    return (flask.json.dumps({"error": error_message}),
            400,
            {'ContentType': 'application/json'})


# Modified from original route for React frontend.
@app.route("/api/delete-tweet-template", methods=["POST"])
def delete_template_for_user_react():
    """Deletes a specific template owned by user."""

    temp_to_del = request.get_json().get("templateId", "")

    if temp_to_del:
        current_user.delete_template(temp_to_del)
        return (flask.json.dumps({'success': True}),
                200,
                {'ContentType': 'application/json'})

    error_message = "Did not receive templateId."
    return (flask.json.dumps({"error": error_message}),
            400,
            {'ContentType': 'application/json'})


# Modified from original route for React frontend.
@app.route("/api/edit-tweet-template", methods=["POST"])
def edit_template_for_user_react():
    """Edits a specific template owned by a user."""
    temp_to_edit = request.get_json().get("templateId", "")
    contents = request.get_json().get("contents", "")

    if temp_to_edit and contents:
        contents = temp_help.replace_nl_with_carriage(contents)
        current_user.edit_template(temp_to_edit, contents)
        return (flask.json.dumps({'success': True}),
                200,
                {'ContentType': 'application/json'})

    error_message = "Bad request. Please send templateId and contents."
    return (flask.json.dumps({"error": error_message}),
            400,
            {'ContentType': 'application/json'})


@app.route("/api/start-tweeting", methods=["POST"])
def start_tweets_react():
    """Starts sending tweets; used for testing."""
    if twitch_helpers.is_twitch_online(current_user):
        # Starts job to fetch twitch data.
        # TODO: UNCOMMENT AFTER TESTING TWITTER HELPERS.
        handler.start_fetching_twitch_data(current_user.user_id)

        # Start sending tweets
        current_user.is_tweeting = True
        tweet_interval = current_user.tweet_interval or 30
        handler.start_tweeting(current_user.user_id, tweet_interval)

        return jsonify(success=True)

    error_message = "User's stream is offline. Jobs not started."
    print(error_message)
    return (flask.json.dumps({"error": error_message}),
            503,
            {'ContentType': 'application/json'})


@app.route("/api/update-user-settings", methods=["POST"])
def update_user_settings_react():
    """Updates settings for a user."""
    new_tweet_interval = request.get_json().get("tweetInterval")

    try:
        new_tweet_interval = int(new_tweet_interval)
    except ValueError:
        error_message = "Tweet interval must be a number."
        print(error_message)
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    if new_tweet_interval < 30:
        error_message = "Tweet interval cannot be less than 30."
        print(error_message)
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    current_user.update_tweet_interval(new_tweet_interval)
    print("\nUpdated user's tweet interval to {}".format(
        current_user.tweet_interval
    ))
    return jsonify(success="Tweet interval updated.")


@app.route("/api/revoke-twitter", methods=["POST"])
def revoke_twitter_access_react():
    """Removes the Twitter token info for a user."""

    user_id = request.get_json().get("userId")

    if not current_user.user_id == int(user_id):
        error_message = "Twitter Token not revoked."
        print(error_message)
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    current_user.remove_twitter_access_token()
    return jsonify(success="Twitter Token removed.")


@app.route("/api/streams")
def get_stream_sessions_for_user_react():
    """Retrives stream session data for user."""

    # Restrict access to logged in users.
    if not current_user.is_authenticated:
        error_message = "You must be logged in to access."
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    started_at = None
    ts = request.args.get("ts")

    try:
        # Default limit to 5 when not given
        limit = int(request.args.get("limit", 5))
        if ts:
            ts = int(ts)
            started_at = datetime.datetime.utcfromtimestamp(ts)
    except ValueError:
        error_message = "Bad request."
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    # Sets a maximum limit of 5
    if limit > 5:
        limit = 5

    return(jsonify(api_helpers.create_streams_payload(
                   user=current_user,
                   dt=started_at,
                   limit=limit)))


@app.route("/api/streams/data/<int:stream_id>")
def get_stream_session_data_react(stream_id):
    """Retrives data points for a given stream session. """

    # Restrict access to logged in users.
    if not current_user.is_authenticated:
        error_message = "You must be logged in to access."
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    payload = api_helpers.create_streamdata_payload(current_user, stream_id)
    if not payload:
        error_message = "No data exists."
        return (flask.json.dumps({"error": error_message}),
                404,
                {'ContentType': 'application/json'})

    return(jsonify(payload))


@app.route("/api/clips/<int:clip_id>")
def get_clip_data_react(clip_id):
    """Retrieves clip data for a given clip id."""

    payload = api_helpers.create_clip_payload(clip_id)

    if not payload:
        error_message = "No data exists."
        return (flask.json.dumps({"error": error_message}),
                404,
                {'ContentType': 'application/json'})

    return(jsonify(payload))


@app.route("/api/sent-tweets")
def get_sent_tweets_for_user_react():
    """Retrieves sent tweet data for user."""

    # Restrict access to logged in users.
    if not current_user.is_authenticated:
        error_message = "You must be logged in to access."
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    started_at_ts = request.args.get("startedAt")  # Timestamp
    ended_at_ts = request.args.get("endedAt")      # Timestamp

    if ended_at_ts == "null":
        ended_at_ts = datetime.datetime.utcnow().timestamp()

    try:
        started_at_ts = int(started_at_ts)
        ended_at_ts = int(ended_at_ts)

        started_at = datetime.datetime.utcfromtimestamp(started_at_ts)
        ended_at = datetime.datetime.utcfromtimestamp(ended_at_ts)
    except ValueError:
        error_message = "Bad request."
        return (flask.json.dumps({"error": error_message}),
                400,
                {'ContentType': 'application/json'})

    tweets = current_user.sent_tweets.filter(SentTweet.created_at.between(
                  started_at, ended_at)).all()

    print(f"STARTED AT: {started_at}")
    print(f"ENDED AT: {ended_at}")

    print(f"\nFOUND TWEETS: {tweets}")

    return(jsonify(api_helpers.create_senttweets_payload(
                   user=current_user,
                   started=started_at,
                   ended=ended_at)))


@app.route("/api/hooks/streamstatus/<int:user_id>", methods=["POST"])
def test_webhook(user_id):
    """Prints webhook response payload. """
    print("Data from Twitch: {}".format(request.get_json()))
    print("User {} stream state has changed.".format(user_id))

    # Extract signature from parameters.
    signature = request.headers.get('X-Hub-Signature')
    if signature:
        signature = signature.split("=")[1]

    body_json = request.get_json()
    body_raw = request.get_data()

    t = Thread(target=process_webhook_request,
               args=(user_id, body_json, body_raw, signature))
    t.start()

    return ('', 200)


def process_webhook_request(user_id, body_json, body_raw, signature):
    """Carries out tasks based on webhook request asynchronously."""

    with app.app_context():
        user = User.query.get(user_id)
        if twitch_helpers.is_auth_signature(body_raw, signature):
            if body_json.get("data"):
                print("\n\nSTARTING DATA FETCH NOW FOR USER {}.\n\n"
                      .format(user_id))
                # Starts job to fetch twitch data.
                handler.start_fetching_twitch_data(user_id)

                if user.is_tweeting:
                    print("\n\nSTARTING TWEETING NOW FOR USER {}.\n\n"
                          .format(user_id))
                    # Start sending tweets
                    tweet_interval = user.tweet_interval or 30
                    handler.start_tweeting(user_id, tweet_interval)
            else:
                print("\n\nENDING JOBS NOW FOR USER {}.\n\n".format(user_id))
                # Stop gathering twitch data and stop tweeting.
                handler.stop_fetching_twitch_data(user_id)
                handler.stop_tweeting(user_id)


@app.route("/api/hooks/streamstatus/<int:user_id>", methods=["GET"])
def test_webhook_get(user_id):
    """Echos back challenge for subscribing."""
    print("Webhook Request: {}".format(list(request.args.items())))

    if request.args.get("hub.mode") == "subscribe":
        print("Subscribing to webhook for {}.".format(user_id))
        challenge = request.args.get("hub.challenge")
        return make_response(challenge)
    else:
        print("Subscription to webhook unsuccessful.")
        return ('', 204)

###############################################################################
# PAGE ROUTES
###############################################################################


@app.route("/")
def show_index():
    "Show homepage."
    if current_user:
        return render_template("add-tweet-template.html")

    return render_template("index.html")


@app.route("/index-react")
def show_index_react():
    "Show homepage using React."

    return render_template("index-react.html")


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
    temp_help.add_basic_templates(new_user)

    # Subscribes to webhooks for user.
    twitch_helpers.subscribe_to_user_stream_events(new_user)
    # Starts job to renew subscription every 9 days.
    handler.renew_webhook(new_user.user_id)

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
    print(callback_uri)


    print("\n\nAt /login/twitch\n\n")
    print("\nNext URL is: {}".format(request.referrer))
    session["referrer_url"] = request.referrer
    return (twitch.authorize(callback=callback_uri,
                             next=request.args.get("next") or
                             request.referrer or None))


@app.route("/login/twitch/authorized")
@twitch.authorized_handler
def authorize_twitch(resp):
    """Get access token from Twitch user after auth."""
    print("\n\nAt /login/twitch/authorized\n\n")
    print("\nNext URL is: {}".format(request.args.get("next")))

    next_url = request.args.get('next') or url_for('show_index')

    # Redirect with message if user does not authorize Twitch account.
    if resp is None:
        # flash('You denied the request to sign in.')
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
        # And renew webhook subscription.
        else:
            print("Twitch ID recognized. Logging you in.")
            login_user(User.get_user_from_twitch_id(current_twitch_user_id))
            current_user.update_twitch_access_token(
                access_token,
                refresh_token,
                expires_in
            )

            # Renews webhook subscription
            twitch_helpers.subscribe_to_user_stream_events(current_user)
            # Starts/replaces job to renew subscription every 9 days.
            handler.renew_webhook(current_user.user_id)

            flask.next = request.args.get('next')
            return (redirect(session["referrer_url"] or
                    flask.next or url_for('show_index')))


@app.route("/logout")
def logout_user_cleanup():
    """Logs out user."""

    print("\n\nGot to logout from: {}".format(request.referrer))

    logout_user()
    session.clear()

    flash("You were logged out!")
    return redirect(request.referrer)


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
    populated_tweet_template = temp_help.populate_tweet_template(template_contents,
                                                                 current_user.user_id)
    if populated_tweet_template:
    # Post the tweet to Twitter
    # TODO: UNCOMMENT WHEN DONE TESTING TWITCH API
    #
        # publish_to_twitter(populated_tweet_template,
        #                    current_user.twitter_token.access_token,
        #                    current_user.twitter_token.access_token_secret,
        #                    current_user.user_id)

        # Currently sending back the populated tweet for confirmation alert.abs

        # TODO: WORK IN PROGRESS
        # Start fetching twitch data
        handler.start_fetching_twitch_data(int(current_user.user_id)) # UNCOMMENT

        # Start sending tweets
        # TODO: Update hardcoded interval to a user's choice.
        tweet_interval = current_user.tweet_interval
        handler.start_tweeting(int(current_user.user_id), tweet_interval)

        return populated_tweet_template

    # TODO: Error handler for case when stream is offline.
    return "Stream is offline."


@app.route("/auth-twitter")
def authorize_twitter():
    """Authorize a user's Twitter account."""
    TWITTER_REDIRECT_URL = url_for("get_twitter_token", _external=True)
    twitter_oauth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                        TWITTER_CONSUMER_SECRET,
                                        TWITTER_REDIRECT_URL)
    print("\n\nGot to auth twitter route.")
    try:
        redirect_url = twitter_oauth.get_authorization_url()
        session["twitter_request_token"] = twitter_oauth.request_token
        # Store referrer url in session so we can redirect
        # back to React frontend after auth flow.
        session["referrer_url"] = request.referrer
        print("\n\nTrying to auth twitter.")
        return redirect(redirect_url)
    except tweepy.TweepError as e:
        print("Twitter authorization failed.")
        print(e.reason)
        return redirect(session["referrer_url"] or "/")


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
        current_user.update_twitter_access_token(access_token,
                                                 access_token_secret)
        print("Twitter account connected.")
    except tweepy.TweepError as e:
        print("Twitter authorization failed.")
        print(e.reason)

    return redirect(session["referrer_url"] or "/")

###############################################################################
# TEST ROUTES
###############################################################################


# @app.route("/webhooktest", methods=["POST"])
# def test_webhook():
#     """Prints webhook response payload. """
#     print("Webhook Request: {}".format(request.get_json()))
#     print("User stream state has changed.")

#     return ('', 204)


# @app.route("/webhooktest", methods=["GET"])
# def test_webhook_get():
#     """Echos back challenge for subscribing."""
#     print("Webhook Request: {}".format(list(request.args.items())))

#     if request.args.get("hub.mode") == "subscribe":
#         print("Successfully subscribed to webhook.")
#         return (request.args.get("hub.challenge"))
#     else:
#         print("Subscription to webhook unsuccessful.")
#         return ('', 204)


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
    from app_globals import scheduler
    # Debug mode enabled for Flask Debug Toolbar
    # app.debug = True
    # Don't cache templates.
    # app.jinja_env.auto_reload = app.debug

    # Scheduler config
    class Config(object):
        """Configuration for APScheduler."""

        SCHEDULER_JOBSTORES = {
            'default': SQLAlchemyJobStore(url='postgresql:///yattk_jobstore')
        }

        SCHEDULER_API_ENABLED = False

    app.config.from_object(Config())

    # Connect to db
    connect_to_db(app)

    # Use Debug Toolbar
    # DebugToolbarExtension(app)

    # Enable scheduler

    scheduler.init_app(app)
    scheduler.start()
    # Run the app
    app.run(port=7000, threaded=True, host='0.0.0.0')
