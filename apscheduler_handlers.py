"""APScheduler job handlers."""
from app_globals import scheduler
import apscheduler_jobs as jobs


def start_fetching_twitch_data(user_id):
    """Begin fetching data about a user's stream."""

    print(user_id)
    scheduler.add_job(func=jobs.fetch_twitch_data,
                      id=str(user_id),
                      trigger="interval",
                      args=[user_id],
                      replace_existing=True,
                      seconds=10)


def stop_fetching_twitch_data(user_id):
    """End the currently running job for the user."""
    scheduler.delete_job(str(user_id))
