"""Seed testdb for Yet Another Twitch Toolkit for interactive use."""
import atexit
import server
import model as m

m.connect_to_db(server.app, "postgresql:///testdb")

m.db.create_all()
m.db.session.commit()
m.sample_data()


@atexit.register
def teardown():
    """Drop all tables in db."""
    m.db.session.close()
    m.db.drop_all()
