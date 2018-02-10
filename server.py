"""Yet Another Twitch Toolkit."""

import os
import bcrypt
import flask
from flask import (Flask, flash,
                   render_template, redirect,
                   request, session, url_for)
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_oauthlib.client import OAuth
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
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


###############################################################################
# ROUTES
###############################################################################


@app.route("/")
def show_index():
    "Show homepage."
    if current_user:
        return render_template("add-tweet-template.html")
    return render_template("index.html")


@app.route("/register", methods=["GET"])
def show_user_registration():
    """Show user registration form."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def process_user_registration():
    """Process user registration form."""

    submitted_email = request.form.get("email").lower()
    submitted_password = request.form.get("password").encode("utf-8")

    if is_email_exists(submitted_email):
        flash("Sorry. That email address is taken.")
        return redirect("/register")

    else:
        hashed_password = bcrypt.hashpw(submitted_password,
                                        bcrypt.gensalt()) \
                          .decode("utf-8")

        new_user = User(email=submitted_email,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Add base templates for user.
        add_basic_templates(new_user)
        flash("Account created successfully.")
        return redirect("/")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user_process():
    """Handles submitted data for user login."""
    # TODO: Write tests.
    submitted_email = request.form.get("email")
    submitted_password = request.form.get("password")

    if is_valid_credentials(submitted_email, submitted_password):
        authed_user = get_user_from_email(submitted_email)
        login_user(authed_user)
        flask.next = request.args.get('next')
        # # Add user_id to session
        # session["user_id"] = current_user.user_id

        return redirect(flask.next or flask.url_for('show_index'))
    else:
        return redirect("/login")


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

    template_contents = request.form.get("template_contents", "").strip()
    if template_contents:
        flash("You entered something!")
        add_template_to_db(current_user, template_contents)
    else:
        flash("You didn't enter anything.")

    return redirect("/")


@app.route("/webhooktest", methods=["POST"])
def test_webhook():
    """Prints webhook response payload. """
    print("Webhook Request: {}".format(request.get_json()))
    print("User stream state has changed.")

    return ('', 204)

###############################################################################
# TEST ROUTES
###############################################################################


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


@app.route("/login-twitch")
def login_with_twitch():
    """Test to login to to app with Twitch account."""
    print("url_for result: {}".format(url_for("get_twitch_access_token")))
    callback_uri = url_for("get_twitch_access_token", _external=True)
    print(callback_uri)
    return (twitch.authorize(callback=callback_uri,
            next=request.args.get("next") or request.referrer or None))


@app.route("/login-twitch-authorized")
def get_twitch_access_token():
    """Get access token from Twitch user after auth."""
    next_url = request.args.get('next') or url_for('show_index')
    resp = twitch.authorized_response()

    # Redirect with message if user does not authorize Twitch account.
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    
    session["twitch_access_token"] = (resp.get("access_token"), "")
    current_twitch_user = twitch.get("users")
    if current_twitch_user.status == 200:
        current_twitch_user = current_twitch_user.data["data"][0]
        print(current_twitch_user)

    return ('', 204)


@twitch.tokengetter
def get_twitch_access_token_from_session():
    return session.get('twitch_access_token')

###############################################################################
# HELPER FUNCTIONS
###############################################################################


@login_manager.user_loader
def load_user(user_id):
    """Loads user from db. user_id must be unicode."""
    print("Found user {}".format(User.query.get(user_id)))
    return User.query.get(user_id)


def add_template_to_db(current_user, temp_contents):
    """Adds a user-created template to db for user."""

    new_template = Template(contents=temp_contents)
    db.session.add(new_template)
    db.session.commit()

    new_user_template = UserTemplate(user_id=current_user.user_id,
                                     template_id=new_template.template_id)
    db.session.add(new_user_template)
    db.session.commit()


def get_user_from_email(user_email):
    """Find the user id for the given email."""

    return User.query.filter_by(email=user_email).one()


def is_email_exists(submitted_email):
    """Check if email is already registered."""

    emails = db.session.query(User.email).all()

    for email in emails:
        if submitted_email in email:
            return True
    return False


def is_valid_credentials(submitted_email, submitted_password):
    """Check to see if submitted password matches hashed password for user."""
    # TODO: Write test.
    user = User.query.filter_by(email=submitted_email).first()

    if user:
        return bcrypt.checkpw(submitted_password.encode("utf-8"),
                              user.password.encode("utf-8"))
    else:
        return False


def add_basic_templates(current_user):
    """Add basic templates for current user."""

    base_templates = Template.query.filter_by(base_template=True)

    temps_to_add = [(UserTemplate(user_id=current_user.user_id,
                                  template_id=base_template.template_id))
                    for base_template in base_templates]

    db.session.bulk_save_objects(temps_to_add)
    db.session.commit()


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
