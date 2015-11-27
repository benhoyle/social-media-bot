# Import json parsing library
import json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Import "ConfigParser" library to load settings ("configparser" in python 3)
from ConfigParser import SafeConfigParser

# Load API variables from settings.cfg file
parser = SafeConfigParser()
parser.read('settings.cfg')

settings_dict = dict(parser.items('twitter_settings'))

oauth = OAuth(settings_dict['access_token'], settings_dict['access_secret'], settings_dict['consumer_key'], settings_dict['consumer_secret'])

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)
            
# Search for latest tweets about query term
print twitter.search.tweets(q='satan')