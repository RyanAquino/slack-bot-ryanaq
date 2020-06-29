"""
Author: Ryan Aquino
Description: Python program that gets the top 10 trending twitter post and post it to slack channel every 3 hours
"""
from config import ACCESS_SECRET, ACCESS_TOKEN, API_SECRET, API_KEY, HOOK_URL
from twitter import Twitter
from slack import Slack
import schedule
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


def main():
    try:
        tweet = Twitter(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        slack = Slack(HOOK_URL)
    except Exception:
        print('Something went wrong')

    trends = tweet.get_trends()
    bubble_sort(trends)
    trends = filter_top10(trends)

    msg = format_tweet(trends)
    slack.post_to_channel(msg)

    print(f'Posted - {time.strftime("%T", time.localtime())}')


schedule.every(3).hour.do(main)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
