"""
Twitter Class for getting top trending tweets around the world.
"""
from tweepy import API
from tweepy import OAuthHandler


class Twitter:

    def __init__(self, api_key, api_secret, access_token, access_secret):
        """
        Authenticate to Twitter API

        :param api_key: twitter developer api key
        :param api_secret: twitter developer api secret key
        :param access_token:  twitter developer access token
        :param access_secret:  twitter developer access token secret
        """
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.ACCESS_TOKEN = access_token
        self.ACCESS_SECRET = access_secret

        auth = OAuthHandler(self.API_KEY, self.API_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_SECRET)
        api = API(auth)

        self.api = api
        self.tweets = None

    def get_trends(self) -> list:
        """
        Get top 50 trending tweets on twitter.com

        :return:  list of top 50 tweets
        """
        list_tweets = self.api.trends_place(1)
        list_tweets = list(list_tweets[0]['trends'])

        self.tweets = list_tweets

        return self.tweets

    def sort_tweets(self) -> None:
        """
        Sort the tweets based on tweet volume using bubble sort alg.

        :return: None
        """
        n = len(self.tweets)

        for i in range(n):
            for j in range(n - 1 - i):
                if not self.tweets[j + 1]['tweet_volume']:
                    self.tweets[j + 1]['tweet_volume'] = 0
                if not self.tweets[j]['tweet_volume']:
                    self.tweets[j]['tweet_volume'] = 0

                if self.tweets[j + 1]['tweet_volume'] > self.tweets[j]['tweet_volume']:
                    self.tweets[j], self.tweets[j + 1] = self.tweets[j + 1], self.tweets[j]

    def filter_top_10(self) -> list:
        """
        Filter top 50 trending tweets to top 10 based on tweet volume

        :param tweets: list of tweets
        :return: list of top 10 tweets
        """

        result = []

        for i in range(10):
            data = {
                'name': self.tweets[i]['name'],
                'url': self.tweets[i]['url'],
                'tweet_volume': self.tweets[i]['tweet_volume']
            }
            result.append(data)

        return result
