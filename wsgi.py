from server import app
from model import connect_to_db
from app_globals import scheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class Config(object):
    """Configuration for APScheduler."""

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='postgresql:///yattk_jobstore')
    }
    SCHEDULER_API_ENABLED = False

app.config.from_object(Config())

# Connect to db
connect_to_db(app)

# Enable scheduler
scheduler.init_app(app)
scheduler.start()
