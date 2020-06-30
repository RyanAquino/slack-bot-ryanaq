"""
Author: Ryan Aquino
Description: Python program that gets the top 10 trending twitter post and post it to slack channel every 3 hours
"""
from config import ACCESS_SECRET, ACCESS_TOKEN, API_SECRET, API_KEY, HOOK_URL, OAUTH
from twitter import Twitter
from slack_bot import Slack
from slack import RTMClient
import threading
import time


def format_tweet(tweets) -> str:
    """
    Format tweets to single string top 10 trends

    :param tweets: list of tweets
    :return: single string of top 10 twitter trends
    """
    msg = ''
    for tweet in range(len(tweets)):
        msg += f'{tweet+1}. {tweets[tweet]["name"]} - {tweets[tweet]["url"]} - {tweets[tweet]["tweet_volume"]} tweets \n'

    return msg.rstrip('\n')


def bubble_sort(data) -> None:
    """
    Sort the tweets based on tweet volume using bubble sort alg.

    :param data: list of tweets
    :return: None
    """
    n = len(data)

    for i in range(n):
        for j in range(n-1-i):
            if not data[j+1]['tweet_volume']:
                data[j+1]['tweet_volume'] = 0
            if not data[j]['tweet_volume']:
                data[j]['tweet_volume'] = 0

            if data[j+1]['tweet_volume'] > data[j]['tweet_volume']:
                data[j], data[j+1] = data[j+1], data[j]


def filter_top10(tweets) -> list:
    """
    Filter top 50 trending tweets to top 10 based on tweet volume

    :param tweets: list of tweets
    :return: list of top 10 tweets
    """

    result = []

    for i in range(10):
        data = {
            'name': tweets[i]['name'],
            'url': tweets[i]['url'],
            'tweet_volume': tweets[i]['tweet_volume']
        }
        result.append(data)

    return result


@RTMClient.run_on(event="message")
def bot(**payload):
    trends = get_top_10()
    msg = format_tweet(trends)
    data = payload['data']
    web_client = payload['web_client']

    if 'trend' in data['text'].lower():
      channel_id = data['channel']
      thread_ts = data['ts']
      user = data['user']

      web_client.chat_postMessage(
        channel=channel_id,
        text=f"Hi <@{user}>! \n Here is the top 10 trending twitter tweets: \n {msg}",
        thread_ts=thread_ts
      )


def get_top_10() -> list:
    """
    Retreive top 10 trending twitter posts
    :return: list
    """
    tweet = Twitter(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    trends = tweet.get_trends()
    bubble_sort(trends)
    trends = filter_top10(trends)

    return trends


def post_to_channel() -> None:
    t = threading.Timer(10800.0, post_to_channel)
    t.daemon = True
    t.start()

    slack = Slack(HOOK_URL)
    trends = get_top_10()
    msg = format_tweet(trends)
    slack.post_to_channel(msg)

    print(f'Posted - {time.strftime("%T", time.localtime())}')


if __name__ == '__main__':
    post_to_channel()
    rtm_client = RTMClient(token=OAUTH)
    rtm_client.start()
