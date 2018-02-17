"""Seed testdb for Yet Another Twitch Toolkit for interactive use."""
import atexit
import server
from model import *

connect_to_db(server.app, "postgresql:///testdb")

db.create_all()
db.session.commit()
sample_data()
import pdb; pdb.set_trace()

@atexit.register
def teardown():
    """Drop all tables in db."""
    db.session.close()
    db.drop_all()
