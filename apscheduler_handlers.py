"""APScheduler job handlers."""
import datetime
import random
from app_globals import scheduler
import apscheduler_jobs as jobs
import twitch_helpers
import template_helpers
import model


def start_fetching_twitch_data(user_id):
    """Begin fetching data about a user's stream."""

    # Do the first run of the task immediately
    user = model.User.get_user_from_id(user_id)
    stream_data = twitch_helpers.serialize_twitch_stream_data(user)
    print(stream_data)
    if stream_data:
        twitch_helpers.write_twitch_stream_data(user, stream_data)

    # Start job on 60 second interval
    interval = 60
    print("Fetching data for user: {}".format(user_id))
    job_type = "fetch_data"
    job_id = job_type + str(user_id)
    scheduler.add_job(func=jobs.fetch_twitch_data,
                      id=job_id,
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      seconds=interval)


def renew_webhook(user_id):
    """Begin renewing webhook subscription for user's stream on interval."""

    interval = 9
    job_type = "renew_webhook"
    job_id = job_type + str(user_id)

    # Start job on 9 day interval
    scheduler.add_job(func=jobs.renew_stream_webhook,
                      id=job_id,
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      days=interval)


def stop_renew_webhook(user_id):
    """End the webhook renewal job."""

    user_id = str(user_id)
    job_type = "renew_webhook"
    stop_job(job_type, user_id)


def stop_fetching_twitch_data(user_id):
    """End the currently running fetch_data job for the user."""
    # Save end timestamp of stream session to close session.
    user = model.User.get_user_from_id(user_id)
    model.StreamSession.end_stream_session(user, datetime.datetime.utcnow())

    user_id = str(user_id)
    job_type = "fetch_data"
    stop_job(job_type, user_id)


def start_tweeting(user_id, interval):
    """Start tweeting for the given user on the specified interval."""

    user = model.User.get_user_from_id(user_id)
    if user.is_tweeting:
        templates = [template.contents for template in user.templates]
        random_template = random.choice(templates)

        tweet_copy = template_helpers.populate_tweet_template(
            random_template, user_id
        )
        if tweet_copy:
            template_helpers.publish_to_twitter(tweet_copy, user_id)

        # Sets up job for tweeting at regular interval.
        job_type = "send_tweets"
        job_id = job_type + str(user_id)
        scheduler.add_job(func=jobs.send_tweets,
                          id=job_id,
                          trigger="interval",
                          args=[user_id],
                          replace_existing=True,
                          minutes=interval)
    else:
        print("\nTweet Job not started; disabled by User {}".format(user_id))


def stop_tweeting(user_id):
    """End the currently running send_tweets job for the user."""
    user_id = str(user_id)
    job_type = "send_tweets"
    stop_job(job_type, user_id)


def stop_job(job_type, user_id):
    """Given a job type and user_id, stop the job."""
    try:
        scheduler.delete_job(job_type + user_id)
    except Exception:
        pass
