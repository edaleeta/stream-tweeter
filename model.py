"""Models and database functions for Yet Another Twitch Toolkit."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################
# MODEL DEFINITIONS
###############################################################################


class User(db.Model):
    """User of Yet Another Twitch Toolkit."""

    # TODO: Not final; need to deal with access tokens, ect.

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)   # Temporary.
    twitch_usrname = db.Column(db.Text, unique=True)
    twitch_id = db.Column(db.Text, unique=True)

    def __repr__(self):
        rep = "<User user_id={}, email={}".format(self.user_id, self.email)
        if self.twitch_usrname:
            rep += ", twitch_usrname={}>".format(self.twitch_usrname)
            return rep
        rep += ">"
        return rep


