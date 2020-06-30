"""
Author: Ryan Aquino
Description: Program that responds to users or post to Slack channel for the top 10 trending tweets in twitter.com for every 3 hours.
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


@RTMClient.run_on(event="message")
def bot(**payload):
    msg = get_top10_msg()
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


def get_top10_msg() -> str:
    """
    Retrieve top 10 trending twitter post and format them into string.

    :return: str
    """
    tweet = Twitter(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    tweet.get_trends()
    tweet.sort_tweets()
    trends = tweet.filter_top_10()
    msg = format_tweet(trends)

    return msg


def post_to_channel() -> None:
    """
    Post to slack channel top 10 trending tweets scheduled every 3 hours.
    :return: None
    """
    t = threading.Timer(10800.0, post_to_channel)
    t.daemon = True
    t.start()

    slack = Slack(HOOK_URL)
    msg = get_top10_msg()
    slack.post_to_channel(msg)

    print(f'Posted - {time.strftime("%T", time.localtime())}')


if __name__ == '__main__':
    post_to_channel()
    rtm_client = RTMClient(token=OAUTH)
    rtm_client.start()
