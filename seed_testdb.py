"""Seed testdb for Yet Another Twitch Toolkit for interactive use."""
import atexit
import server
from model import *

###############################################################################
# SAMPLE DATA
###############################################################################


def sample_data():
    """Create sample data."""

    # Empty existing data
    BaseTemplate.query.delete()
    Template.query.delete()
    TwitchClip.query.delete()
    StreamDatum.query.delete()
    StreamSession.query.delete()
    SentTweet.query.delete()
    User.query.delete()
    db.session.commit()

    # Execute raw SQL to import data from csv's in respective tables.
    project_path = os.getcwd()
    fill_users = ("COPY users FROM '" + project_path +
                  "/sql/users.csv' DELIMITER ','")
    fill_twitch_clips = ("COPY twitch_clips FROM '" +
                         project_path + "/sql/twitch_clips.csv'")
    fill_templates = ("COPY templates FROM '" +
                      project_path + "/sql/templates.csv'")
    fill_stream_sessions = ("COPY stream_sessions FROM '" +
                            project_path + "/sql/stream_sessions.csv'")
    fill_stream_data = ("COPY stream_data FROM '" +
                        project_path + "/sql/stream_data.csv'")
    fill_sent_tweets = ("COPY sent_tweets FROM '" +
                        project_path + "/sql/sent_tweets.csv'")
    fill_base_templates = ("COPY base_templates FROM '" +
                           project_path + "/sql/base_templates.csv'")
    fill_twitch_tokens = ("COPY twitch_tokens FROM '" +
                          project_path + "/sql/twitch_tokens.csv'")

    db.session.execute(fill_base_templates)
    db.session.execute(fill_users)
    db.session.execute(fill_templates)
    db.session.execute(fill_stream_sessions)
    db.session.execute(fill_stream_data)
    db.session.execute(fill_twitch_clips)
    db.session.execute(fill_sent_tweets)
    db.session.execute(fill_twitch_tokens)
    db.session.commit()

    # Add Template entry per base template for each initial user.
    base_templates = BaseTemplate.query
    initial_users = User.query

    for user in initial_users:
        for base_template in base_templates:
            db.session.add(Template(user_id=user.user_id,
                                    contents=base_template.contents))
    db.session.commit()

    # Private functions to set the next values of PKs
    def set_val_user_id():
        """Set value for the next user_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(User.user_id)).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('users_user_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_base_templates_id():
        """Set value for the next template_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            BaseTemplate.template_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('base_templates_template_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_sent_tweet_id():
        """Set value for the next tweet_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            SentTweet.tweet_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('sent_tweets_tweet_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_stream_data_id():
        """Set value for the next data_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            StreamDatum.data_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('stream_data_data_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_stream_id():
        """Set value for the next stream_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            StreamSession.stream_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('stream_sessions_stream_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_template_id():
        """Set value for the next template_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            Template.template_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('templates_template_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_clip_id():
        """Set value for the next clip_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            TwitchClip.clip_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('twitch_clips_clip_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    def set_val_twitch_token_id():
        """Set value for the next Twitch token_id after seeding database."""

        # Get the max id in the database
        result = db.session.query(func.max(
            TwitchToken.token_id
            )).one()
        max_id = int(result[0])

        # Set the value for the next id to be max_id + 1
        query = "SELECT setval('twitch_tokens_token_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()

    # Set next values of PKs where seeded data exists.
    set_val_user_id()
    set_val_base_templates_id()
    set_val_sent_tweet_id()
    set_val_stream_data_id()
    set_val_stream_id()
    set_val_template_id()
    set_val_clip_id()
    set_val_twitch_token_id()

###############################################################################
# SEED DIRECTLY FOR INTERACTIVE MODE
###############################################################################

if __name__ == "__main__":
    connect_to_db(server.app, "postgresql:///testdb")

    db.create_all()
    db.session.commit()
    sample_data()

    @atexit.register
    def teardown():
        """Drop all tables in db."""

        db.session.close()
        db.reflect()
        db.drop_all()
