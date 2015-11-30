# Import random and time libraries
import random, time

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Import "ConfigParser" library to load settings ("configparser" in python 3)
from ConfigParser import SafeConfigParser

# Load API variables from settings.cfg file - needs full path for cron path
parser = SafeConfigParser()
parser.read('/home/pi/social-media-bot/settings.cfg')

settings_dict = dict(parser.items('twitter_settings'))

oauth = OAuth(settings_dict['access_token'], settings_dict['access_secret'], settings_dict['consumer_key'], settings_dict['consumer_secret'])

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)

# Load query term from configuration file
query_term = parser.get('query_settings','query_term')

# Exclude RTs and replies in search query by adding " -RT -@"
expanded_query_term = query_term + ' -RT -filter:replies'

# Load response strings from settings.cfg file
responses = parser.get('response_settings','responses').split(';')
responses = [r.strip().strip("'") for r in responses]

# Load highest tweetID from last set of search results from settings.cfg
last_tweet_id = parser.get('query_settings', 'last_tweet_id')

# Search for latest tweets about query term
# Restrict to English language tweets and recent rather than popular
# Tweets has components 'search_metadata' and 'statuses' - we want the latter
tweets = twitter.search.tweets(q=expanded_query_term, lang='en', result_type='recent', count='15', since_id=last_tweet_id)['statuses']

# Extract tweetID, username and text of tweets returned from search
# Use dictionary comprehension in future iterations?
tweets = [{
			'id_str': tweet['id_str'],
			'screen_name': tweet['user']['screen_name'],
			'original_text': tweet['text'], 
			'response_text': '@' + tweet['user']['screen_name'] + ' ' + random.choice(responses)
			} for tweet in tweets if query_term in tweet['text'].lower()]

#Posting on twitter
for tweet in tweets:
#Leave a random pause (between 55 and 75s long) between posts to avoid rate limits
	twitter.statuses.update(status=tweet['response_text'], in_reply_to_status_id=tweet['id_str'])
	#print tweet['original_text'], '\n', tweet['response_text'],  tweet['id_str']
	time.sleep(random.randint(55,75))

#Don't forget running list of IDs so you don't post twice - maybe use since_id to do this simply - record latest id return by search and start next search from this
id_ints = [int(t['id_str']) for t in tweets]
# Add highest tweetID to settings.cfg file
parser.set('query_settings', 'last_tweet_id', str(max(id_ints)))
# Write updated settings.cfg file
with open('settings.cfg', 'wb') as configfile:
    parser.write(configfile)

#Posting rate limits are 10-15 per 15 minute interval -cron every 15mins then wait one minute between replies