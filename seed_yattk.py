"""Seed testdb for Yet Another Twitch Toolkit for interactive use."""
import server
from model import *

connect_to_db(server.app, "postgresql:///yattk")

db.create_all()
db.session.commit()
sample_data()
