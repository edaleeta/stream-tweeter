"""Yet Another Twitch Toolkit."""

from jinja2 import StrictUndefined
from flask import (Flask, flash,
                   render_template, redirect,
                   request, session)
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Set so we can use Flask's default toolbar
app.secret_key = "18db2d51c63606dece6e98a196c6a262c2026c6f9cbc3e4f"

# Raise an exception if we use an undefined variable in Jinja.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_index():
    "Show homepage."

    return render_template("index.html")


if __name__ == "__main__":
    # Debug mode enabled for Flask Debug Toolbar
    app.debug = True
    # Don't cache templates.
    app.jinja_env.auto_reload = app.debug

    # Use Debug Toolbar
    DebugToolbarExtension(app)

    # Run the app
    app.run(port=7000, host='0.0.0.0')
