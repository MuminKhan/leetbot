import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


slack_web_client = WebClient(token=os.environ.get("ALGOBOT_SLACK_TOKEN"))


def post_to_slack(message):
    response = None
    try:
        response = slack_web_client.chat_postMessage(**message)
    except SlackApiError as e:
        response = f'Request to Slack API Failed: {e.response.status_code}.'

    return response
