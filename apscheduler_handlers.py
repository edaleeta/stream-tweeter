"""APScheduler job handlers."""
from app_globals import scheduler
import apscheduler_jobs as jobs
import twitch_helpers
import template_helpers
import model
import random


def start_fetching_twitch_data(user_id):
    """Begin fetching data about a user's stream."""

    # Do the first run of the task immediately
    user = model.User.get_user_from_id(user_id)
    # twitch_helpers.get_and_write_twitch_stream_data(user)

    # Start job on interval
    interval = 30
    print("Fetching data for user: {}".format(user_id))
    job_type = "fetch_data"
    job_id = job_type + str(user_id)
    scheduler.add_job(func=jobs.fetch_twitch_data,
                      id=job_id,
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      seconds=interval)


def stop_fetching_twitch_data(user_id):
    """End the currently running fetch_data job for the user."""
    user_id = str(user_id)
    job_type = "fetch_data"
    stop_job(job_type, user_id)


def start_tweeting(user_id, interval):
    """Start tweeting for the given user on the specified interval."""

    user = model.User.get_user_from_id(user_id)
    templates = [template.contents for template in user.templates]
    print("\n\nAVAILABLE TEMPLATES: {}\n\n".format(templates))
    random_template = random.choice(templates)
    print("\n\nRandom template is: {}\n\n".format(random_template))
    template_helpers.create_and_publish_to_twitter(random_template,
                                                   user_id)
    print("TWEET TWEETED.")

    # Interval will be defined in minutes.
    # TODO: WORK IN PROGRESS. REMOVE WHEN COMPLETE.
    job_type = "send_tweets"
    job_id = job_type + str(user_id)
    scheduler.add_job(func=jobs.send_tweets,
                      id=job_id,
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      seconds=interval)


def stop_tweeting(user_id):
    """End the currently running send_tweets job for the user."""
    user_id = str(user_id)
    job_type = "send_tweets"
    stop_job(job_type, user_id)


def stop_job(job_type, user_id):
    """Given a job type and user_id, stop the job."""
    scheduler.delete_job(job_type + user_id)
