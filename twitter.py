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

    def get_trends(self) -> list:
        """
        Get top 50 trending tweets on twitter.com

        :return:  list of top 50 tweets
        """
        list_tweets = self.api.trends_place(1)
        list_tweets = list(list_tweets[0]['trends'])

        return list_tweets
