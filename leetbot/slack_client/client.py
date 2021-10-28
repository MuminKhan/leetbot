import os

from slack import WebClient
from slack.errors import SlackApiError
from slack.web.client import WebClient


slack_web_client = WebClient(token=os.environ.get("ALGOBOT_SLACK_TOKEN"))


def post_to_slack(message):
    response = None
    try:
        response = slack_web_client.chat_postMessage(**message)
    except SlackApiError as e:
        response = f'Request to Slack API Failed: {e.response.status_code}.'

    return response
