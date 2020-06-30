"""
Slack class that post the top 10 trending tweets
"""
import requests


class Slack:
    def __init__(self, hook_url):
        self.hook_url = hook_url

    def post_to_channel(self, message):
        """
        Send message to slack channel

        :param message: message to be send
        :return: None
        """
        data = {
            'text': str(message)
        }

        requests.post(self.hook_url, json=data)
