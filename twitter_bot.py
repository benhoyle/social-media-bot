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

# Load query term from configuration file
query_term = parser.get('query_settings','query_term')

#Exclude RTs and replies in search query by adding " -RT -@"
expanded_query_term = query_term + ' -RT -filter:replies'
   
# Search for latest tweets about query term
# Restrict to English language tweets and recent rather than popular
# Tweets has components 'search_metadata' and 'statuses' - we want the latter
tweets = twitter.search.tweets(q=expanded_query_term, lang='en', result_type='recent', count='20')['statuses']

# Extract tweetID, username and text of tweets returned from search
tweets = [[tweet['id_str'],tweet['user']['screen_name'],tweet['text']] for tweet in tweets if query_term in tweet['text'].lower()]

import pprint
pprint.pprint(tweets)

#Posting on twitter
#twitter.statuses.update(status="Hello mortal realm")

#Load response strings from settings.cfg file
responses = parser.get('response_settings','responses')
print responses

#Build replies - add screen_name to start with '@'

#Don't forget running list of IDs so you don't post twice - maybe use since_id to do this simply - record latest id return by search and start next search from this