"""Yet Another Twitch Toolkit."""

import os
import string
import flask
from flask import (Flask, flash, get_template_attribute,
                   render_template, redirect,
                   request, session, url_for)
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_oauthlib.client import OAuth
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import *

# TESTING NL2BR FILTER
import re
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r)?')



app = Flask(__name__)

# Set so we can use Flask's default toolbar
app.secret_key = "18db2d51c63606dece6e98a196c6a262c2026c6f9cbc3e4f"

# Raise an exception if we use an undefined variable in Jinja.
app.jinja_env.undefined = StrictUndefined

# Login manager for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

# Set up requirements for Twitch OAuth2
oauth = OAuth(app)
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

twitch = oauth.remote_app(
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


# TESTING NL2BR
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

###############################################################################
# ROUTES
###############################################################################


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

    return populate_tweet_template(template_contents)

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


def populate_tweet_template(contents):
    """Inserts data into placeholders."""
    # TODO: Update to use data received through Twitch API.

    mock_stream_data = {"game": "Pokemon Silver",
                        "url": "http://twitch.tv/the_pixxel",
                        "viewers": 180,
                        "stream_desc": "Thowback - Starting Pokemon Silver!"}
    tweet_template = string.Template(contents)
    populated_template = tweet_template.safe_substitute(mock_stream_data)
    return populated_template


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
