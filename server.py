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

    return render_template("index.html")


@app.route("/register", methods=['GET'])
def show_user_registration():
    """Show user registration form."""

    return render_template("register.html")


@app.route("/register", methods=['POST'])
def process_user_registration():
    """Process user registration form."""

    submitted_email = request.form.get("email")
    submitted_password = request.form.get("password").encode("utf-8")

    if is_email_exists(submitted_email):
        flash("Sorry. That email address is taken.")
        return redirect("/register")

    else:
        hashed_password = bcrypt.hashpw(submitted_password, bcrypt.gensalt(10))

        new_user = User(email=submitted_email,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Add base templates for user.
        add_basic_templates(new_user)
        flash("Account created successfully.")
        return redirect("/")

###############################################################################
# HELPER FUNCTIONS
###############################################################################


def is_email_exists(submitted_email):
    """Check if email is already registered."""

    # TODO: Update to use User object.
    emails = db.session.query(User.email).all()

    for email in emails:
        if submitted_email in email:
            return True
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
