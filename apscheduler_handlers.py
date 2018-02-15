"""APScheduler job handlers."""
from app_globals import scheduler
import apscheduler_jobs as jobs


def start_fetching_twitch_data(user_id):
    """Begin fetching data about a user's stream."""

    print("Fetching data for user: {}".format(user_id))
    job_type = "fetch_data"
    job_id = job_type + str(user_id)
    scheduler.add_job(func=jobs.fetch_twitch_data,
                      id=job_id,
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      seconds=10)


def stop_fetching_twitch_data(user_id):
    """End the currently running fetch_data job for the user."""
    user_id = str(user_id)
    job_type = "fetch_data"
    stop_job(job_type, user_id)


def stop_job(job_type, user_id):
    """Given a job type and user_id, stop the job."""
    scheduler.delete_job(job_type + user_id)
