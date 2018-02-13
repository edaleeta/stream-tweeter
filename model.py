"""Models and database functions for Yet Another Twitch Toolkit."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

###############################################################################
# MODEL DEFINITIONS
###############################################################################


class User(db.Model):
    """User of Yet Another Twitch Toolkit."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    twitch_displayname = db.Column(db.Text)
    twitch_username = db.Column(db.Text)
    twitch_id = db.Column(db.Text, unique=True)
    twitter_id = db.Column(db.Text, unique=True)

    is_active = True
    is_authenticated = True
    is_anonymous = False

    @staticmethod
    def get_user_from_email(user_email):
        """Find the user for the given email."""

        return User.query.filter_by(email=user_email).one()

    @staticmethod
    def get_user_from_twitch_id(twitch_id):
        """Find the user for the given Twitch ID."""

        return User.query.filter_by(twitch_id=twitch_id).one()

    def __repr__(self):
        """Print helpful information."""

        rep = "<User user_id={}, email='{}'".format(self.user_id, self.email)
        if self.twitch_username:
            rep += ", twitch_username='{}'>".format(self.twitch_username)
            return rep
        rep += ">"
        return rep

    def get_id(self):
        """Return a unicode string; for flask-login."""
        return str(self.user_id)

    def update_twitch_access_token(self,
                                   access_token,
                                   refresh_token,
                                   expires_in):
        """Updates the Twitch access token and info for user."""
        my_token = self.twitch_token
        if my_token:
            my_token.access_token = access_token
            my_token.refresh_token = refresh_token
            my_token.expires_in = expires_in
        else:
            new_token = TwitchToken(
                user_id=self.user_id,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in
            )
            db.session.add(new_token)
        db.session.commit()

    def delete_template(self, template_id):
        """Allows a user to delete an owned template."""
        temp_to_del = Template.query.filter_by(template_id=template_id,
                                               user_id=self.user_id).one()
        db.session.delete(temp_to_del)
        db.session.commit()

    def edit_template(self, template_id, new_contents):
        """Allows a user to edit an owned template."""
        temp_to_edit = Template.query.filter_by(template_id=template_id,
                                                user_id=self.user_id).one()
        temp_to_edit.contents = new_contents
        db.session.commit()


class TwitchToken(db.Model):
    """Twitch access tokens for a user."""

    __tablename__ = "twitch_tokens"

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    access_token = db.Column(db.Text,
                             unique=True,
                             nullable=False)
    refresh_token = db.Column(db.Text,
                              unique=True,
                              nullable=False)
    expires_in = db.Column(db.Integer)

    user = db.relationship("User",
                           backref=backref("twitch_token", uselist=False))

    def __repr__(self):
        """Print helpful information."""

        if self.twitter_token:
            twitter_token_exists = "True"
        else:
            twitter_token_exists = "False"

        return "<AccessToken twitter_exists={}>" \
            .format(twitter_token_exists)


class Template(db.Model):
    """Template used for Tweets."""

    __tablename__ = "templates"

    template_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    contents = db.Column(db.Text, nullable=False)

    user = db.relationship("User",
                           backref=backref("templates",
                                           order_by="Template.template_id"),
                           uselist=False)

    @staticmethod
    def get_template_from_id(template_id):
        """Find the template for the given template_id."""

        return Template.query.filter_by(template_id=template_id).one()


class BaseTemplate(db.Model):
    """Base templates used to create templates for user upon user creation."""

    __tablename__ = "base_templates"

    template_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Print helpful information."""

        return "<Template template_id={}, user_id={}, contents='{}'>" \
            .format(self.template_id,
                    self.user_id,
                    (self.contents[0:14] + "..."))


class SentTweet(db.Model):
    """Tweets created and sent."""

    __tablename__ = "sent_tweets"

    tweet_id = db.Column(db.Integer, primary_key=True)
    tweet_twtr_id = db.Column(db.Text, nullable=False, unique=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    permalink = db.Column(db.Text, nullable=False)
    clip_id = db.Column(db.Integer, db.ForeignKey("twitch_clips.clip_id"))

    user = db.relationship("User",
                           backref="sent_tweets")
    clip = db.relationship("TwitchClip", back_populates="tweet", uselist=False)

    def __repr__(self):
        """Print helpful information."""

        return "<SentTweet tweet_id='{}', user_id={}, message='{}'>" \
            .format(self.tweet_id, self.user_id, (self.message[0:14] + "..."))


class StreamSession(db.Model):
    """A Twitch Stream session."""

    __tablename__ = "stream_session"

    stream_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    twitch_session_id = db.Column(db.String(16), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    ended_at = db.Column(db.DateTime)

    feedback = db.relationship("StreamSessionUserFeedback",
                               back_populates="session",
                               uselist=False)

    def __repr__(self):
        """Print helpful information."""

        return "<StreamSession stream_id={}, twitch_session_id='{}', \
            started={}>".format(self.data_id,
                                self.twitch_session_id,
                                self.started_at)


class StreamDatum(db.Model):
    """Data gathered from Twitch when user is live."""

    __tablename__ = "stream_data"

    data_id = db.Column(db.Integer, primary_key=True)
    stream_id = db.Column(db.Integer,
                          db.ForeignKey("stream_session.stream_id"),
                          nullable=False)
    game_played = db.Column(db.String(50), nullable=False)
    stream_title = db.Column(db.String(140), nullable=False)
    viewer_count = db.Column(db.Integer, nullable=False)

    session = db.relationship("StreamSession",
                              backref="data")

    def __repr__(self):
        """Print helpful information."""

        return "<StreamDatum data_id={}, twitch_id='{}', v_count={}>" \
            .format(self.data_id, self.twitch_id, self.viewer_count)


class TwitchClip(db.Model):
    """Clips auto-generated for Tweets."""

    __tablename__ = "twitch_clips"

    clip_id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Text, nullable=False)
    stream_id = db.Column(db.Integer,
                          db.ForeignKey("stream_session.stream_id"),
                          nullable=False)

    session = db.relationship("StreamSession",
                              backref="clips")
    tweet = db.relationship("SentTweet", back_populates="clip", uselist=False)

    def __repr__(self):
        """Print helpful information."""

        return "<TwitchClip clip_id={}, slug='{}'>"


class StreamSessionUserFeedback(db.Model):
    """Stores user-input for stream session."""

    __tablename__ = "stream_session_user_feedback"

    feedback_id = db.Column(db.Integer,
                            primary_key=True)
    stream_id = db.Column(db.Integer,
                          db.ForeignKey("stream_session.stream_id"),
                          nullable=False)
    mood_rating = db.Column(db.Integer)
    notes = db.Column(db.Text)

    session = db.relationship("StreamSession",
                              back_populates="feedback",
                              uselist=False)

    def __repr__(self):
        """Print helpful information."""

        return "<StreamLogEntry feedback_id={}, stream_id={}>" \
            .format(self.feedback_id, self.stream_id)

###############################################################################
# SAMPLE DATA
###############################################################################


def sample_data():
    """Create sample data."""

    # Empty existing data
    BaseTemplate.query.delete()
    User.query.delete()
    Template.query.delete()

    # Add sample users
    # TODO: Update this so user creation doesn't fail. :)
    user_1 = User(email="test@testing.com")
    user_2 = User(email="eda@leeta.com")
    db.session.add_all([user_1, user_2])
    db.session.commit()

    # Add base templates
    template_1 = BaseTemplate(contents="I'm live on Twitch!\r\n \
        Join me here: $url.")
    template_2 = BaseTemplate(contents="We're playing $game!\r\nJoin me on \
        Twitch: $url.")

    db.session.add_all([template_1, template_2])
    db.session.commit()

    # Add Template entry per base template for each initial user.
    base_templates = BaseTemplate.query
    initial_users = User.query

    for user in initial_users:
        for base_template in base_templates:
            db.session.add(Template(user_id=user.user_id,
                                    contents=base_template.contents))
    db.session.commit()

###############################################################################
# HELPER FUNCTIONS
###############################################################################


def connect_to_db(app, db_uri="postgresql:///yattk", show_sql=True):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = show_sql
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
