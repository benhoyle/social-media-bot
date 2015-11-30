# social-media-bot
Playing around with automated social media entities.

The python script uses a settings.cfg file structured as follows:

[twitter_settings]
ACCESS_TOKEN = [Your token here]
ACCESS_SECRET = [Your secret here]
CONSUMER_KEY = [Your key here]
CONSUMER_SECRET = [Your secret here]

[query_settings]
query_term = [Your query term here]
last_tweet_id = 0

[response_settings]
responses =
	'String phrase 1.';
	'String phrase 2.';
	'String phrase 3.'

The script then searches for tweets containing the query term. A reply is then posted from the account associated with the token, key and secrets. The reply randomly selects one of the string phrases in the responses section. The reply is posted as a reply to tweets that contain the query term.

I have the script scheduled as a cron job that runs every 20 minutes. I had to hard-code the path to the settings.cfg file to get this cron job working - you may need to modify for your own path.