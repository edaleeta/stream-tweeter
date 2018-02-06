"""Models and database functions for Yet Another Twitch Toolkit."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################
# MODEL DEFINITIONS
###############################################################################


class User(db.Model):
    """User of Yet Another Twitch Toolkit."""

    # TODO: Not final; need to deal with access tokens, ect.
    # Will break into seperate table.

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)   # Temporary.
    twitch_usrname = db.Column(db.Text, unique=True)
    twitch_id = db.Column(db.Text, unique=True)
    twitter_id = db.Column(db.Text, unique=True)

    templates = db.relationship("Template",
                                secondary="users_templates",
                                backref="users")

    def __repr__(self):
        """Print helpful information."""

        rep = "<User user_id={}, email='{}'".format(self.user_id, self.email)
        if self.twitch_usrname:
            rep += ", twitch_usrname='{}'>".format(self.twitch_usrname)
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

    __tablename__ = "templates"

    template_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Print helpful information."""

        return "<Template template_id={}, contents='{}'>" \
            .format(self.template_id, (self.contents[0:14] + "..."))


class SentTweet(db.Model):
    """Tweets created and sent."""

    __tablename__ = "sent_tweets"

    tweet_id = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    created_at = db.Column(db.Timestamp, nullable=False)
    message = db.Column(db.Text, nullable=False)
    permalink = db.Column(db.Text, nullable=False)
    clip_id = db.Column(db.Integer, db.ForeignKey("twitch_clips.clip_id"))

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
    started_at = db.Column(db.Timestamp, nullable=False)
    ended_at = db.Column(db.Timestamp)

    log_entry = db.relationship("StreamLogEntry",
                                backref="stream_sessions")

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
    stream_id = db.Column(db.String(16),
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

    def __repr__(self):
        """Print helpful information."""

        return "<TwitchClip clip_id={}, slug='{}'>"


class StreamLogEntry(db.Model):
    """Entry for the live stream log."""

    __tablename__ = "stream_log_entries"

    entry_id = db.Column(db.Integer,
                         primary_key=True)
    stream_id = db.Column(db.Integer,
                          db.ForeignKey("stream_session.stream_id"),
                          nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    mood_rating = db.Column(db.Integer)
    notes = db.Column(db.Text)

    user = db.relationship("User",
                           backref="log_entries")

    def __repr__(self):
        """Print helpful information."""

        return "<StreamLogEntry stream_id={}, user_id={}>" \
            .format(self.stream_id, self.user_id)
