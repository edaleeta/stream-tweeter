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

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)   # Temporary.
    twitch_usrname = db.Column(db.Text, unique=True)
    twitch_id = db.Column(db.Text, unique=True)

    templates = db.relationship("Template",
                                secondary="users_templates",
                                backref="users")

    def __repr__(self):
        """Print helpful information."""

        rep = "<User user_id={}, email={}".format(self.user_id, self.email)
        if self.twitch_usrname:
            rep += ", twitch_usrname={}>".format(self.twitch_usrname)
            return rep
        rep += ">"
        return rep


class UserTemplate(db.Model):
    """User to Template associations."""

    __tablename__ = "users_templates"

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        primary_key=True,
                        autoincrement=False)

    template_id = db.Column(db.Integer,
                            db.ForeignKey("templates.template_id"),
                            primary_key=True,
                            autoincrement=False)

    def __repr__(self):
        """Print helpful information."""

        return "<UserTemplate user_id={}, template_id={}>" \
            .format(self.user_id, self.template_id)


class Template(db.Model):
    """Template used for Tweets."""

    template_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Print helpful information."""

        return "<Template template_id={}, contents(trunc)={}>" \
            .format(self.template_id, self.contents[0:14])
