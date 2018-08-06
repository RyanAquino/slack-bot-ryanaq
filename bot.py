'''Slackbot program that post top 10 trending tweets on twitter'''

import time
import re
import config
from tweepy import API
from tweepy import OAuthHandler
from operator import itemgetter
from slackclient import SlackClient
from threading import Timer

config.slack_client = SlackClient(config.slack_client)

starterbot_id = None
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
tryInput = 'post trending'

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    default_response = "Not sure what you mean. Try *{}*.".format(tryInput)

    if command.startswith("post"):
        response ="Top 10 trending tweets: \n" + twitter_trend()
    else:
        response = default_response

    config.slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

def sendResponse():
    config.slack_client.api_call(
        "chat.postMessage",
        channel='assignment1',
        text="Top 10 trending tweets: \n" + twitter_trend()
    )
    Timer(86400,sendResponse).start()

def twitter_trend():
    auth = OAuthHandler(config.key,config.secret)
    auth.set_access_token(config.token,config.secret1)
    api = API(auth)

    listTweets = api.trends_place(1)
    sortedTweets = []

    trends = listTweets[0]
    temp_trends = trends['trends']

    for trnd in temp_trends:
        sortedTweets.append(trnd)

    sortedTweets = sorted(sortedTweets, key=itemgetter('tweet_volume'),reverse=True)

    ctr = 1
    top10 = []

    for test in sortedTweets:
        if ctr <= 10:
            top10.append(str(ctr) + '. ' + test['name'])
            ctr +=1

    trending10 = ' \n'.join(top10)
    return trending10

if __name__ == "__main__":
    if config.slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        sendResponse()

        starterbot_id = config.slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(config.slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed! Try again")


