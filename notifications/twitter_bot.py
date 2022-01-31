import tweepy as tw

CONSUMER_KEY = 'zoWK3og8WN10OLecodekgUExk'
CONSUMER_SECRET = 'wsXSj1mqi0cWwwhvFWYmraF4VWznda3hrqqFY6PUQM0aDdNjbf'
ACCESS_KEY = '964632632482062337-xCfzmgaNUvx1G0R6yD3AdVuTrlcwrug'
ACCESS_SECRET = 'nzY0hEo2PD0MjsnyjRyTCYvUXJRYl0lz7gTTXwzAZnI8A'

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)


def stream(tag):

    tweets = tw.Cursor(api.search, q=tag, lang="en",
                       tweet_mode='extended').items(2)

    list_tweets = [tweet for tweet in tweets]
    # print(list_tweets)
    i = 1
    tweet_dict = {}
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        datetime = f'{tweet.created_at.year}-{tweet.created_at.month}-{tweet.created_at.day}'
        id = str(tweet.id[:6])
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text

        vars = ('username', 'description', 'text', 'datetime')
        vars2 = (str(username), str(description), str(text), datetime)
        if id not in tweet_dict.keys():
            tweet_dict[id] = tuple(zip(vars, vars2))
        i += 1

    return tweet_dict


print(stream('messi'))
