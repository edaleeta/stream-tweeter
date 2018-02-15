"""Sandbox for APScheduler."""

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db

db = SQLAlchemy()

if __name__ == "__main__":
    from server import app

    # app.config.from_object(Config())

    connect_to_db(app)

    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()

    app.run(port=7000, host="0.0.0.0")