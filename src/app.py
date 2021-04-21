import logging
import os
import schedule
import time

from flask import Flask
from slack import WebClient
from slack.errors import SlackApiError
from slack.web.client import WebClient

from algobot import AlgoBot

# slack info
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))
slack_channel = "slack-dev"

def get_message():
    bot = AlgoBot(slack_channel, "test/example_manifest.json")
    message = bot.get_message_payload()
    
    return message

def post_to_slack(slack_client, message):
  try:
    slack_client.chat_postMessage(channel=slack_channel, text=message)
  except SlackApiError as e:
    logging.error(f'Request to Slack API Failed: {e.response.status_code}.')
    logging.error(e.response)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    
    schedule.every().day.at("9:00").do(post_to_slack(slack_web_client, get_message()))

