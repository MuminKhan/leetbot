from utils.config import config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_web_client = WebClient(token=config.slack_token)


def post_to_slack(message):
    response: dict = None
    try:
        slack_response = slack_web_client.chat_postMessage(**message)
        response = {
            "status": "success",
            "status_code": slack_response.status_code,
            "data": slack_response.data,
            "message": "Message posted successfully.",
        }
    except SlackApiError as e:
        response = {
            "status": "error",
            "status_code": e.response.status_code,
            "data": e.response.data,
            "message": e.args[0],
        }

    return response
