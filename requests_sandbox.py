"""Sandbox to try out requests."""
import os
import sys
import requests as req
from requests_oauthlib import OAuth2Session


TWITCH_LOGIN = "the_pixxel"
payload = {"login": "the_pixxel"}

try:
    TWITCH_CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
except KeyError:
    print("Please set the environment variable TWITCH_CLIENT_ID")
    sys.exit(1)

headers = {"Client-ID": TWITCH_CLIENT_ID}
url = "https://api.twitch.tv/helix/users"

r = req.get(url,
            params=payload,
            headers=headers)
