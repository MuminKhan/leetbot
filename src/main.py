import argparse
import logging
import os

from slack import WebClient
from slack.errors import SlackApiError
from slack.web.client import WebClient

from studybot import StudyBot

# slack info
slack_web_client = WebClient(token=os.environ.get("ALGOBOT_SLACK_TOKEN"))

def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument('--channel',  '-c', required=True,  dest='channel',       action='store', help='Channel to post to. Bot must be a member to post.')
  parser.add_argument('--manifest', '-m', required=True,  dest='manifest_file', action='store', help='Location of manifest file. Must be a .csv or .json.')
  parser.add_argument('--template', '-t', required=True,  dest='template_file', action='store', help='Template file location') 

  args = parser.parse_args()
  return args

def post_to_slack(slack_client, message):
  response = None
  try:
    response = slack_client.chat_postMessage(**message)
  except SlackApiError as e:
    logging.error(f'Request to Slack API Failed: {e.response.status_code}.')
    logging.error(e.response)
  
  return response


if __name__ == "__main__":
    args = parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    
    bot = StudyBot(args.channel, args.manifest_file, args.template_file)
    message = bot.get_message_payload()

    if message is not None:
      response = post_to_slack(slack_web_client, message)
    else:
      print('Nothing to post...')

    print(f"\n\n\nRESPONSE: \n{str(response)}") if response is not None else print('')