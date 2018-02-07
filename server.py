"""Yet Another Twitch Toolkit."""

import bcrypt
from flask import (Flask, flash,
                   render_template, redirect,
                   request, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import *

app = Flask(__name__)

# Set so we can use Flask's default toolbar
app.secret_key = "18db2d51c63606dece6e98a196c6a262c2026c6f9cbc3e4f"

# Raise an exception if we use an undefined variable in Jinja.
app.jinja_env.undefined = StrictUndefined

###############################################################################
# ROUTES
###############################################################################


@app.route("/")
def show_index():
    "Show homepage."
    if session.get("user_id"):
        current_user = get_user_from_session()

        return render_template("index.html",
                               user=current_user)

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
def login_user():
    """Handles submitted data for user login."""
    # TODO: Write tests.
    submitted_email = request.form.get("email")
    submitted_password = request.form.get("password")

    if is_valid_credentials(submitted_email, submitted_password):
        current_user = get_user_from_email(submitted_email)
        current_user.isLoggedIn = True
        # Add user_id to session
        session["user_id"] = current_user.user_id
        return redirect("/")
    else:
        flash("Incorrect credentials. Please try again.")
        return redirect("/login")


@app.route("/logout")
def logout_user():
    """Logs out user."""

    get_user_from_session().isLoggedIn = False
    session.clear()
    flash("You were logged out!")
    return redirect("/")


###############################################################################
# HELPER FUNCTIONS
###############################################################################


def get_user_from_session():
    """Find the current user object based on current session."""
    current_user_id = session.get("user_id")
    current_user = User.query.filter_by(user_id=current_user_id).first()
    return current_user


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
