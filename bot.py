import time
import re

from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from operator import itemgetter
import config

starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "123"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith("do post"):
        response = twitter_trend()

    #Sends the response back to the channel
    config.slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )



def twitter_trend():
    def on_data(self, raw_data):
        print raw_data
        return True

    def on_error(self, status_code):
        print status_code

    auth = OAuthHandler(config.key,config.secret)
    auth.set_access_token(config.token,config.secret1)
    twitterStream = Stream(auth,StreamListener)
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
            top10.append(test['name'])
            ctr +=1

    trending10 = ', \n'.join(top10)

    return trending10

if __name__ == "__main__":
    if config.slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = config.slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(config.slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


