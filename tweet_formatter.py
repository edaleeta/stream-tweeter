"""Formatting sandbox for Tweet Temapltes"""
from string import Formatter, Template
import re

TEMPLATE_STRING = "Hey there, I'm playing ${game}! Join me at ${url}"
OTHER_TEMPLATE_STRING = "I'm live on #Twitch! ${stream_desc} at ${url}"
NORMAL_STRING = "I'm just a string that expects reg formatting. Game: {}"
GAME = "Pokemon"


my_tweet = Template(TEMPLATE_STRING)
my_other_tweet = Template(OTHER_TEMPLATE_STRING)

# If I wanted a list of tuples of identifiers in the template, I could use
# the following regex.

# identifiers = re.findall(r'^(?=.*\${(url)})(?=.*\${(game)}).*$',
#                          TEMPLATE_STRING)


# Possible placeholders:
# ${game}
# ${url}
# ${viewers}
# ${stream_desc}

stream_data = {"game": GAME,
               "url": "http://twitch.tv/the_pixxel",
               "viewers": 180,
               "stream_desc": "Starting Pokemon Silver!"}

print(my_tweet.safe_substitute(stream_data))
print(my_other_tweet.safe_substitute(stream_data))
