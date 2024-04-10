import os
import logging

#import tweepy

logger = logging.getLogger("twitter")

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
        tweet_list.append(tweet_dict)

    return tweet_list


#if __name__ == "__main__":
#    print(scrape_user_tweets(username="hwchase17"))

if __name__ == "__main__":
    import tweepy
    import pandas as pd

    # consumer_key = "************" #Your API/Consumer key
    # consumer_secret = "*********" #Your API/Consumer Secret Key
    # access_token = "***********"    #Your Access token key
    # access_token_secret = "*************" #Your Access token Secret key

    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
    consumer_key = os.environ["TWITTER_API_KEY"]
    consumer_secret = os.environ["TWITTER_API_KEY_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    # Pass in our twitter API authentication key
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret,
        access_token, access_token_secret
    )

    # Instantiate the tweepy API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    search_query = "'ref''world cup'-filter:retweets AND -filter:replies AND -filter:links"
    no_of_tweets = 100

    try:
        # The number of tweets we want to retrieved from the search
        tweets = api.search_tweets(q=search_query, lang="en", count=no_of_tweets, tweet_mode='extended')

        # Pulling Some attributes from the tweet
        attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for
                                tweet in tweets]

        # Creation of column list to rename the columns in the dataframe
        columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]

        # Creation of Dataframe
        tweets_df = pd.DataFrame(attributes_container, columns=columns)
    except BaseException as e:
        print('Status Failed On,', str(e))
