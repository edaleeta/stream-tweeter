"""Models and database functions for Yet Another Twitch Toolkit."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################
# MODEL DEFINITIONS
###############################################################################


class User(db.Model):
    """User of Yet Another Twitch Toolkit."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    twitch_displayname = db.Column(db.Text, nullable=False)
    twitch_username = db.Column(db.Text)
    twitch_id = db.Column(db.Text, unique=True)
    twitter_id = db.Column(db.Text, unique=True)

    templates = db.relationship("Template",
                                secondary="users_templates",
                                backref="users")

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


class TwitchToken(db.Model):
    """Twitch access tokens for a user."""
    # TODO: Store these encrypted.

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
                           backref="twitch_tokens")

    def __repr__(self):
        """Print helpful information."""

        if self.twitter_token:
            twitter_token_exists = "True"
        else:
            twitter_token_exists = "False" 

        return "<AccessToken twitter_exists={}>" \
            .format(twitter_token_exists)


class UserTemplate(db.Model):
    """User to Template associations."""

    __tablename__ = "users_templates"

    user_template_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))

    template_id = db.Column(db.Integer,
                            db.ForeignKey("templates.template_id"))

    def __repr__(self):
        """Print helpful information."""

        return "<UserTemplate user_id={}, template_id={}>" \
            .format(self.user_id, self.template_id)


class Template(db.Model):
    """Template used for Tweets."""

    __tablename__ = "templates"

    template_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)
    base_template = db.Column(db.Boolean)

    def __repr__(self):
        """Print helpful information."""

        return "<Template template_id={}, contents='{}'>" \
            .format(self.template_id, (self.contents[0:14] + "..."))


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
    UserTemplate.query.delete()
    User.query.delete()
    Template.query.delete()

    # Add sample users
    user_1 = User(email="test@testing.com")
    user_2 = User(email="eda@leeta.com")
    db.session.add_all([user_1, user_2])
    db.session.commit()

    # Add base templates
    template_1 = Template(contents="I'm live on Twitch!\r\n \
        Join me here: $url.",
                          base_template=True)
    template_2 = Template(contents="We're playing $game!\r\nJoin me on \
        Twitch: $url.",
                          base_template=True)
    template_3 = Template(contents="This should not be initialized for User.")

    db.session.add_all([template_1, template_2, template_3])
    db.session.commit()

    # Add UserTemplates entry per base template for each initial user.
    base_templates = Template.query.filter_by(base_template=True)
    initial_users = User.query

    for user in initial_users:
        for base_template in base_templates:
            db.session.add(UserTemplate(user_id=user.user_id,
                                        template_id=base_template.template_id))
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
